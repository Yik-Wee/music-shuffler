import requests
import json


playlist_id = 'PLUQKJP1sVuNMvxOYqmdyOkE8Ryd_AWbQT'

# timeout after 30 seconds
res = requests.get(f'http://127.0.0.1:5000/api/playlist/youtube?id={playlist_id}', timeout=30)
print(res)
res_json = res.json()
if not res.ok:
    print(f'Failed to get contents of playlist {playlist_id}')

print(json.dumps(res_json, indent=2))
