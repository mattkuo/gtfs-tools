#!/usr/bin/env python

import sqlite3
import python
import sys


def write_routes(sqlite):
    bin_file = open(sys.argv[2] + "/routes", "wb")
    cursor = sqlite.execute("SELECT route_id, route_short, route_long_name FROM routes")
    routes = python.Routes_pb2.Routes()

    for row in cursor:
        short_name = row["route_short"]
        # Exclude routes 8xx, 9xx and P25
        if short_name[0] == "8" or short_name[0] == "9" or short_name[0] == "P":
            continue
        print "Working on Route %s" % short_name
        a_route = routes.routes.add()
        a_route.route_short = short_name
        a_route.route_long = row["route_long_name"]

        write_shapes(sqlite, short_name, row["route_id"])
        write_route_data(sqlite, short_name, row["route_id"])

    bin_file.write(routes.SerializeToString())
    bin_file.close()

# Given a route_id find all the stops associated with that route
def write_route_data(sqlite, route_short, route_id):
    print "--> Stops for %s" % route_short
    route_data = python.RouteData_pb2.RouteData()

    query = """SELECT DISTINCT stops.stop_code, trips.direction_id FROM trips
            JOIN stop_times ON stop_times.trip_id=trips.trip_id
            JOIN stops ON stops.stop_id=stop_times.stop_id
            WHERE trips.route_id=?"""

    cursor = sqlite.execute(query, (route_id,))
    for row in cursor:
        if row["direction_id"] == "0":
            route_data.stops0.append(int(row["stop_code"]))
        else:
            route_data.stops1.append(int(row["stop_code"]))

    route_data_file = open(sys.argv[2] + "/" + route_short + ".rd", "wb")
    route_data_file.write(route_data.SerializeToString())
    route_data_file.close()

def write_stops(sqlite):
    print "--> Working on writing stops"
    cursor = sqlite.execute("SELECT stop_code, stop_name, stop_lat, stop_lon FROM stops")
    stops = python.Stops_pb2.Stops()

    for row in cursor:
        a_stop = stops.stops.add()

        if isinstance(row["stop_code"], int):
            a_stop.stop_code = int(row["stop_code"])
        a_stop.stop_name = row["stop_name"]
        a_stop.coordinate.latitude = row["stop_lat"]
        a_stop.coordinate.longitude = row["stop_lon"]

    stops_file = open(sys.argv[2] + "/stops", "wb")
    stops_file.write(stops.SerializeToString())
    stops_file.close()


def write_shapes(sqlite, route_short, route_id):
    print "--> Shape for %s" % route_short
    cursor = sqlite.execute("SELECT DISTINCT trips.shape_id FROM trips WHERE trips.route_id=?", (route_id,))
    shape = python.Shape_pb2.Shape()

    for row in cursor:
        a_path = shape.path.add()
        shape_id = row["shape_id"]

        coord_cursor = sqlite.execute("SELECT shape_pt_lat, shape_pt_lon FROM shapes WHERE shape_id=?", (shape_id,))

        for coords in coord_cursor:
            a_coordinate = a_path.coordinates.add()
            a_coordinate.latitude = coords["shape_pt_lat"]
            a_coordinate.longitude = coords["shape_pt_lon"]

    shape_file = open(sys.argv[2] + "/" + route_short + ".shape", "wb")
    shape_file.write(shape.SerializeToString())
    shape_file.close()


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s %s %s" % (sys.argv[0], "SQLITE_FILE", "OUTPUT_FOLDER")
        sys.exit(-1)

    sqlite = sqlite3.connect(sys.argv[1])
    sqlite.row_factory = sqlite3.Row
    write_routes(sqlite)
    write_stops(sqlite)
