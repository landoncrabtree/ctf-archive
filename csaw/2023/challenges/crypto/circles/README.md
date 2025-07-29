# Circles

## Description

We have this encrypted file and the only information we got is that the key follows the pattern of `1,2,4,8,16,...`. Can you figure out what the key is and decrypt this file?

Author: `Dhyey Shah (CTFd)`

## Files

* [flag.enc](files/flag.enc)

* [server.py](files/server.py)

## Solution

We are given an encrypted file along with the code that was used to encrypt it. From this, we know AES-256 CBC was used because of `to_bytes(32,"big")`. Additionally, we know the IV is `r4nd0m_1v_ch053n`. 

All we are missing the key. From the description, the key follows the geometric sequence `1,2,4,8,16,...`. First intuition is the geometric sequence:

```
f(x) = 2^(x-1)
f(1) = 2^0 = 1
f(2) = 2^1 = 2
f(3) = 2^2 = 4
```

We can automate the process of decrypting by bruteforcing. The logic is as follows:

1. Generate a key using the geometric sequence
2. Decrypt the file using the generated key
3. Ensure the decrypted file has the PNG header

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
with open('flag.enc','rb') as f:
	data = f.read()

for i in range(1,5000):
    key = (2**(i-1)).to_bytes(32,"big")
    iv = b"r4nd0m_1v_ch053n"
    cipher = AES.new(key, AES.MODE_CBC, iv)
    dec = cipher.decrypt(data)
    if dec[:4] == b"\x89PNG":
        with open('flag.dec','wb') as f:
            f.write(dec)
```

However, this fails to decrypt the file properly. Referencing back to the challenge, "circle" stood out to me. Some Googling of "1,2,4,8,16 circle" revealed [Dividing a circle into areas](https://en.wikipedia.org/wiki/Dividing_a_circle_into_areas) which also follows the geometric sequence `1,2,4,8,16,...`. The sequence is OEIS [A000127](https://oeis.org/A000127). Visiting the page, we are fortunate to find sample Python on how to generate the sequence:

```python
return n*(n*(n*(n - 6) + 23) - 18)//24 + 1
```

Another thing I thought about was the need to bruteforce. I felt that I shouldn't need to bruteforce the key. Looking back at `server.py`, I realized they gave us the `n` for the sequence: `0xcafed3adb3ef1e37`. Putting it all together, our final decryption script is:

```python
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad


def A000127(n):
    return  n*(n*(n*(n - 6) + 23) - 18)//24 + 1

iv = b"r4nd0m_1v_ch053n"
key = A000127(0xcafed3adb3ef1e37)
key_bytes = key.to_bytes(32, "big")
print(str(key))

with open('flag.enc', 'rb') as f:
    data = f.read()

cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
dec = cipher.decrypt(data)
if dec[0:4] == b"\x89\x50\x4e\x47":
    print("challenge solved get rekt lol")
    with open('flag.png', 'wb') as f:
        f.write(dec)
```

Running the script, we get the flag:

`csawctf{p4773rn5_c4n_b3_d3c31v1n6.5h0u70u7_70_3blu31br0wn_f0r_7h3_1d34}`

