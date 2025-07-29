url1 = 'http://web.csaw.io:14180/identity/images?user=%22otacon@protonmail.com%22'
url2 = 'http://web.csaw.io:14180/identity/images?user=%22solidsnake@protonmail.com%22'

import requests

r1 = requests.get(url1, verify=False)
r2 = requests.get(url2, verify=False)

resp1 = r1.json()
resp2 = r2.json()

for i in resp1['msg']:
    url = 'http://web.csaw.io:14180/images/' + i['filename']
    # download the file
    r = requests.get(url, verify=False)
    with open(i['filename'], 'wb') as f:
        f.write(r.content)

for i in resp2['msg']:
    url = 'http://web.csaw.io:14180/images/' + i['filename']
    # download the file
    r = requests.get(url, verify=False)
    with open(i['filename'], 'wb') as f:
        f.write(r.content)