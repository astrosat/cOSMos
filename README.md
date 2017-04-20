# cOSMos package for OSM data retrieval
**cOSMos** is a thin wrapper for [OSM overpass API](http://wiki.openstreetmap.org/wiki/Overpass_API) that provides a number of helper functions to make downloading particular Open Street Map data easier. It allows to extract common features of interest (road networks, city locations, building footprints) based on location name.

# Install
```bash
pip install cosmos-osm
```

# Using from shell
Location defined on instantiation.
```python
from cosmos import Data

data = Data('Krakow')

roads = data.get('roads', format='geojson')
```

Location passed as argument.
```python
from cosmos import Data

data = Data()

cities = data.get('cities', 'Scotland', format='geojson')
roads = data.get('roads', 'Kuala Lumpur', format='geojson')
```

Location defined by bbox.
```python
south = 47.3202203,
west = 8.4480061
north = 47.4346662
east = 8.6254413
zurich = (south, west, north, east)

# Without format argument it will return 2 generators with geometries and tags.
buildings, tags = data.get('buildings', bbox=zurich)
```

# Using from command line
From terminal:
```bash
cosmos --location=Musselburgh --filename=musselburgh_roads.geojson
```
Will create musselburgh_roads.geojson GeoJSON file with road network for Musselburgh. Here's `--help` output:
```bash
Usage: cosmos [OPTIONS]

Options:
  --location TEXT                 input location name(city, country)
  --filename TEXT                 output file name
  --dtype [roads|cities|buildings]
                                  data type
  --bbox <FLOAT FLOAT FLOAT FLOAT>...
                                  bbox in form (lat1, lon1, lat2, lon2)
  --help                          Show this message and exit.
```

# Data types
Currently implemented data types than can be extracted with **cOSMos**

| Name | Geometry | Example |
|------|----------|---------|
| Roads| LineString| `data.get('roads', 'London')`|
| Cities| Point | `data.get('cities', 'Portugal')`|
| Buildings | Polygon | `data.get('buildings', 'Prague')`|

# Dependencies
cOSMos uses a number of awesome python packages, please check their websites:

* [geopy](https://github.com/geopy/geopy)
* [python-geojson](https://github.com/frewsxcv/python-geojson)
* [click](http://click.pocoo.org/5/)
* [requests](http://docs.python-requests.org/en/master/)
* [shapely](http://toblerity.org/shapely/)
