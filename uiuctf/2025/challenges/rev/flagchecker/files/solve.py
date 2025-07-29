from sympy.ntheory import discrete_log

MOD = 0xffffff2f

# Convert bytes to uint32 list (little endian)
def bytes_to_u32_list(b):
    return [int.from_bytes(b[i:i+4], 'little') for i in range(0, len(b), 4)]

test_pt = bytes_to_u32_list(b"\xf5\xb1e\"JX\xb7\x91\xdfj\xf1\xd80>a\xcd\xc4\xbb\x86\xc3\xd1\xc4'\x10<4LA\x89\xeb/\x1e")
test_ct = bytes_to_u32_list(b"^\xbfD\xdc\xec\x1c\xffZ\xc2\xb4\xe9\xe1\x92\x9b2\x01*\xa9\x9c\x8f\xb4\xc5E\x0e\x91KJ`Y\xeb\x81p")
flag_enc = bytes_to_u32_list(b"\x11\x91\x18$E\xe9\x94\xfd\xa6d\x9f\x1b\xa3\xe9\xec\x7f\xde\x0e*\xfc\xf5\xdcnW\x9cL\xe4\x01\x90\xf7\x8ae")

# Solve for input[i]
inputs = []
for i, (pt, ct) in enumerate(zip(test_pt, test_ct)):
    x = discrete_log(MOD, ct, pt)
    print(f"input[{i}] = {x}")
    inputs.append(x)

# Decode flag
def F(base, exp, mod=MOD):
    result = 1
    base = base % mod
    while exp > 0:
        if exp & 1:
            result = (result * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return result

flag_parts = [F(enc, exp) for enc, exp in zip(flag_enc, inputs)]
flag_bytes = b''.join(x.to_bytes(4, 'little') for x in flag_parts)

print("Flag:", flag_bytes.decode(errors="ignore"))  # ignore errors in case of non-UTF8
