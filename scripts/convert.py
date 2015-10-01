#!/usr/bin/python
import sys
import os
import sqlite3

def insert_data(db, table, gtfs_file):
    f = open(gtfs_file).read().split("\n")
    gtfs_data = [tuple(row.split(",")) for row in f]
    num_columns = len(gtfs_data[0])
    placeholder = ', '.join('?' * num_columns)

    for row in gtfs_data[1:]:
        if len(row) == num_columns:
            db.execute("INSERT INTO %s VALUES (%s)" % (table, placeholder), row)

    db.commit()
    print "Finished inserting into %s using %s" % (table, gtfs_file)


def create_db(db):
    # db.execute("CREATE TABLE agency (agency_url TEXT, agency_name TEXT, agency_timezone TEXT, agency_id TEXT, agency_lang TEXT);")
    db.execute("CREATE TABLE stops (stop_id INTEGER, stop_code INTEGER, stop_name TEXT, stop_desc TEXT, stop_lat REAL, stop_lon REAL, zone_id INTEGER, stop_url TEXT, location_type INTEGER, parent_station INTEGER);")
    db.execute("CREATE TABLE routes (route_id INTEGER, agency_id TEXT, route_short TEXT, route_long_name TEXT, route_desc TEXT, route_type INTEGER, route_url TEXT, route_color TEXT, route_text_color TEXT);")
    db.execute("CREATE TABLE trips (route_id INTEGER, service_id INTEGER, trip_id INTEGER, trip_headsign TEXT, trip_short_name TEXT, direction_id INTEGER, block_id INTEGER, shape_id INTEGER);")
    db.execute("CREATE TABLE calendar (service_id TEXT,start_date TEXT,end_date TEXT, monday BOOLEAN,tuesday BOOLEAN,wednesday BOOLEAN,thursday BOOLEAN,friday BOOLEAN,saturday BOOLEAN,sunday BOOLEAN);")
    db.execute("CREATE TABLE calendar_dates (service_id TEXT, date TEXT, exception_type INTEGER);")
    db.execute("CREATE TABLE shapes (shape_id INTEGER, shape_pt_lat REAL, shape_pt_lon REAL, shape_pt_sequence INTEGER, shape_dist_traveled REAL);")
    db.execute("CREATE TABLE stop_times (trip_id INTEGER, arrival_time TEXT, departure_time TEXT, stop_id INTEGER, stop_sequence INTEGER, stop_headsign TEXT, pickup_type INTEGER, drop_off_type INTEGER, shape_dist_traveled REAL);")
    db.commit()

def main(argv):
    path = argv[0]
    if not os.path.exists(path):
        open(os.path.abspath(path), 'w').close()
    else:
        sys.stderr.write("Cannot create db file\n")
        sys.exit()

    db = sqlite3.connect(os.path.abspath(path))
    create_db(db)
    # insert_data(db, 'agency', 'agency.txt')
    insert_data(db, 'stops', 'stops.txt')
    insert_data(db, 'routes', 'routes.txt')
    insert_data(db, 'trips', 'trips.txt')
    # insert_data(db, 'calendar', 'calendar.txt')
    # insert_data(db, 'calendar_dates', 'calendar_dates.txt')
    insert_data(db, 'shapes', 'shapes.txt')
    insert_data(db, 'stop_times', 'stop_times.txt')
    db.execute("VACUUM")
    db.close()
    print "Done!"


if __name__ == '__main__':
    main(sys.argv[1:])
