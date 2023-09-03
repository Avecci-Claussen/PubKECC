import hashlib
import random
import ecdsa

def xor_hex(hex1, hex2):
    num1 = int(hex1, 16)
    num2 = int(hex2, 16)
    xor_result = num1 ^ num2
    return format(xor_result, 'x').zfill(len(hex1))

def hamming_weight(x):
    weight = 0
    while x:
        weight += x & 1
        x >>= 1
    return weight

def generate_numbers_with_hamming_weight(n, k, offset=0, val=0, results=[]):
    if k == 0:
        results.append(val)
        return
    if n == 0:
        return
    generate_numbers_with_hamming_weight(n - 1, k, offset + 1, val, results)
    val |= (1 << offset)
    generate_numbers_with_hamming_weight(n - 1, k - 1, offset + 1, val, results)
    val &= ~(1 << offset)

def hash160(public_key):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(public_key)
    rip.update(sha.digest())
    return rip.digest().hex()

min_value = int("20000000000000000", 16)
max_value = int("3ffffffffffffffff", 16)

target_hamming_weight = 38

mask = "0000000000000000000000000000000000000000000000000000000000000001"

generated_keys = set()

while len(generated_keys) < 10000:
    random_num = random.randint(min_value, max_value)
    hex_num = format(random_num, 'x')
    unmasked_key = xor_hex(hex_num, mask)

    weight = hamming_weight(int(unmasked_key, 16))
    if weight == target_hamming_weight:
        generated_keys.add(unmasked_key.zfill(64))

with open("homa.txt", "w") as file:
    for key in generated_keys:
        # Get the public key
        sk = ecdsa.SigningKey.from_string(bytes.fromhex(key), curve=ecdsa.SECP256k1)
        vk = sk.verifying_key
        public_key = b'\x04' + vk.to_string()  # 0x04 for uncompressed key

        generated_hash160 = hash160(public_key)

        if generated_hash160.startswith("20d4"):
            file.write(f"Private Key: {key}, Hash160: {generated_hash160}\n")

print("Hashes and private keys with prefix '20d45a' written to homa.txt")
