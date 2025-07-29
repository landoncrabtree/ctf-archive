import requests
from base64 import b64decode

r = requests.get('http://misc.csaw.io:3003')
flag = r.text
flag = b64decode(flag)

def deobf(int1, int2, int3):
    i = int2 - int1
    arrayOfChar = []
    for int2 in range(i):
        arrayOfChar.append(chr(flag[int1 + int2] ^ int3))
    return ''.join(arrayOfChar)

print(deobf(275, 306, 42))