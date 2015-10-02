# gtfs-tools #

A collection of scripts to parse [General Transit Feed Specification](https://developers.google.com/transit/gtfs/)
into [Protobuf](https://developers.google.com/protocol-buffers/?hl=en) format

There are four main scripts including the Rakefile:

* peuker.py - Implements the [Doug-Peuker Alogrithm](https://en.wikipedia.org/wiki/Ramer%E2%80%93Douglas%E2%80%93Peucker_algorithm) to reduce excess points in shapes.txt. Used for bringing down filesize of shapes.txt while maintaining route shape elegibility. I saw a 60% reduction in filesize. Play around with the epsilon value for optimal results.

* create-sqlite.py - Loads unzipped gtfs data into a sqlite database for easy data querying and viewing

* route-create.py - Queries route and shape information from the SQLite file generated from create-sqlite.py into protobuf files.

* Rakefile - Builds Python and Java proto files.
