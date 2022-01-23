from pprint import pprint

import requests

url = 'https://i.imgur.com/RL7ojOc.jpg'
# url = 'https://image.prntscr.com/image/oWlhVs0HSzuTASbloiRQDA.jpg'
# url = 'https://image.prntscr.com/image/02EZiiOVQIWdCXy-rDosvw.jpeg'
# url = 'https://i.imgur.com/kxUDgpf.png'
# print(requests.get(url, stream=True).headers['Content-length'])

# print(requests.head(url))
response = requests.get(url, stream=True, headers={'User-Agent': 'Mariya'})
# print(response.headers['Content-length'])
# print(response.content)
pprint(response.headers['Content-length'])
pprint(type(response.status_code))

