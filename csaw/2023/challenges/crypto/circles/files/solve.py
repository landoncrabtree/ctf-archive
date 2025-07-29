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
