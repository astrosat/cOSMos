# Overpass API constants
OVERPASS_API_URL = 'http://overpass-api.de/api/interpreter'
JSON_QUERY_TEMPLATE = '[out:json];node({}, {}, {}, {}){};{} out body geom;'
CITY_QUERY = ('["place"~"city|town"]', '')
ROAD_QUERY = ('', 'way(bn)[highway];(._;>;);')
BUILDING_QUERY = ('', 'way(bn)[building];(._;>;);')

# Request configuration constants
RESPONSE_TIMEOUT = 25  # seconds
