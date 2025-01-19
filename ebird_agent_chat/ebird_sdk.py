from pprint import pprint
import json
from ebird.api import (
    get_nearby_hotspots, 
    get_observations,
    get_nearby_observations,
    get_nearby_species,

)

api_key = '62vrn2b53gfe'
locale='zh'
cur_lat,cur_lon = (22.81683353214568, 120.22304445763693)

# nearby = get_nearby_hotspots(api_key, cur_lat, cur_lon, dist=10,back=1)
# pprint(nearby)

# this_week = get_observations(api_key, 'L2619940', back=1,locale='zh')
# pprint(this_week)

records = get_nearby_observations(api_key, cur_lat, cur_lon, dist=20, back=7,locale='zh',hotspot=True,max_results=100)

with open('test/result.json', 'w') as f:
    f.write(f"total: {len(records)}\n")
    json.dump(records, f, ensure_ascii=False, indent=4)


# nearby_species = get_nearby_species(api_key, 'whvmyn', cur_lat, cur_lon,dist=10,locale='zh')
# pprint(nearby_species)



