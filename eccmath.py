from ecdsa import SECP256k1, VerifyingKey
from ecdsa.util import string_to_number, number_to_string

# Convert a compressed public key to a VerifyingKey object
def pubkey_to_vk(pubkey):
    return VerifyingKey.from_string(bytes.fromhex(pubkey[2:]), curve=SECP256k1)

# Convert a VerifyingKey object to a compressed public key
def vk_to_pubkey(vk):
    prefix = '02' if vk.pubkey.point.y() & 1 == 0 else '03'
    return prefix + vk.pubkey.point.x().to_string(format='hex')

# Subtract one public key from another
def subtract_pubkeys(pubkey1, pubkey2):
    vk1 = pubkey_to_vk(pubkey1)
    vk2 = pubkey_to_vk(pubkey2)

    # Get the additive inverse of vk1
    vk1_neg = VerifyingKey.from_public_point(-vk1.pubkey.point, curve=SECP256k1)

    # Add vk1_neg to vk2
    result_point = vk2.pubkey.point + vk1_neg.pubkey.point
    result_vk = VerifyingKey.from_public_point(result_point, curve=SECP256k1)

    return vk_to_pubkey(result_vk)

pubkey1 = '02e0a8b039282faf6fe0fd769cfbc4b6b4cf8758ba68220eac420e32b91ddfa673'
pubkey2 = '035cd1854cae45391ca4ec428cc7e6c7d9984424b954209a8eea197b9e364c05f6'

print(subtract_pubkeys(pubkey1, pubkey2))
