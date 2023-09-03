import hashlib
import ecdsa
import random

def hash160(public_key):
    sha = hashlib.sha256()
    rip = hashlib.new('ripemd160')
    sha.update(public_key)
    rip.update(sha.digest())
    return rip.digest().hex()

def compress_pubkey(pubkey):
    x, y = pubkey.to_string()[:32], pubkey.to_string()[32:]
    prefix = b'\x02' if y[-1] % 2 == 0 else b'\x03'
    return prefix + x

target_hash160s = set()
with open("hfile.txt", "r") as f:
    for line in f:
        target_hash160s.add(line.strip())

min_value = 2 ** 65
max_value = 2 ** 69 - 1

# Create or clear the col.txt file
with open("col.txt", "w") as f:
    f.write("")

while True:
    random_private_key = random.randint(min_value, max_value)
    random_private_key_hex = format(random_private_key, 'x').zfill(64)

    sk = ecdsa.SigningKey.from_string(bytes.fromhex(random_private_key_hex), curve=ecdsa.SECP256k1)
    vk = sk.verifying_key
    uncompressed_pubkey = b'\x04' + vk.to_string()
    compressed_pubkey = compress_pubkey(vk)

    computed_hash160 = hash160(compressed_pubkey)


    if computed_hash160 in target_hash160s:
        print(f"Collision found! Private key: {random_private_key_hex}")
        
        # Write the collision to col.txt
        with open("col.txt", "a") as f:
            f.write(f"{computed_hash160} collides with private key {random_private_key_hex}\n")

        # Remove the found hash from the set
        target_hash160s.remove(computed_hash160)
        
        # If all collisions are found, stop the loop
        if not target_hash160s:
            print("All collisions found!")
            break
