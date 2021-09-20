import requests

API_URL = 'http://127.0.0.1:5000/'

with open('/src/images/an_ugly_building.png') as fp:
    content = fp.read()

response = requests.post(
    '{}/files/an_ugly_building.png'.format(API_URL), headers=headers, data=content
)