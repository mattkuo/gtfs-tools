import sys
import math

class Point():
    """Represents a point on a map"""
    def __init__(self, shape_id, lat, long, point_num, traveled):
        self.lat = lat
        self.long = long
        self.shape_id = shape_id
        self.point_num = point_num
        self.traveled = traveled

    def __str__(self):
        return "shape_id: %s, Lat: %s, Long: %s, point_num: %s" % (self.shape_id,self.lat, self.long, self.point_num)

def peuker(points, epsilon):
    first_point = points[0]
    last_point = points[-1]

    if len(points) <= 2:
        return points

    index = -1
    distance = 0

    for i, point in enumerate(points):
        current_dist = find_perp_dist(point, first_point, last_point);

        if current_dist > distance:
            distance = current_dist
            index = i

    if distance > epsilon:
        line1 = points[:index + 1]
        line2 = points[index:]

        call1 = peuker(line1, epsilon)[:-1]
        call2 = peuker(line2, epsilon)

        call1.extend(call2)
        return call1
    else:
        return [first_point, last_point]

def find_perp_dist(p, p1, p2):
    if p1.long == p2.long:
        result = abs(p.long - p1.long)
    else:
        slope = (p2.lat - p1.lat) / (p2.long - p1.long)
        intercept = p1.lat - (slope * p1.long)
        result = abs(slope * p.long - p.lat + intercept) / math.sqrt(abs(slope) ** 2 + 1)

    return result

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print "Usage: %s %s %s" % (sys.argv[0], "GTFS_TEXT", "NEW_TEXT")
        sys.exit(-1)

    file = open(sys.argv[1])
    new_file = open(sys.argv[2], "w")

    points = []
    current_shape_id = 0

    header = file.readline()
    new_file.write(header)

    for i, line in enumerate(file):
        data = line.split(",")

        if i == 0:
            current_shape_id = data[0]

        if data[0] != current_shape_id:
            result = peuker(points, 0.00005)

            for point in result:
                new_file.write("%s, %s, %s, %s, %s\n" % (point.shape_id, point.lat, point.long, point.point_num, point.traveled))

            current_shape_id = data[0]
            points = []

        point = Point(data[0],float(data[1]), float(data[2]), data[3], float(data[4]))
        points.append(point)

    result = peuker(points, 0.00005)

    for point in result:
        new_file.write("%s, %s, %s, %s, %s\n" % (point.shape_id, point.lat, point.long, point.point_num, point.traveled))

    file.close()
    new_file.close()
