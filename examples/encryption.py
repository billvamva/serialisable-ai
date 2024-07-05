from pkmai.pokemon import PokemonDataEncryption, Pokemon

from pkmai.codec import bytes_to_str, str_to_bytes

# # Provided stream of bytes for Milotic 
# data = b"\x2f\xff\xe0\x36\xa1\x8f\xc9\xaa\xc7\xc3\xc6\xc9\xce\xc3\xbd\xff\x6d\x00\x02\x02\xff\xbb\xce\xff\xff\xff\xff\x00\x92\x28\x00\x00\xee\x71\x1e\x9c\x61\x70\x40\x9c\x80\x69\x39\x8f\xc7\x71\x29\x9c\x32\xd2\x29\x9c\x8e\x4f\x29\x9c\x8e\x4f\x8a\x8d\x51\x8b\xd6\xa3\x8e\xf0\x29\x9c\xdb\x25\x7c\xc9\xdb\x25\x29\x96\x8e\x70\x29\x9c\x00\x00\x00\x00\x1f\xff\x34\x00\x74\x00\x34\x00\x4b\x00\x47\x00\x53\x00\x62\x00"

# # Instantiate PokemonDataEncryption object with original_trainer_id and personality_value
# encryption = PokemonDataEncryption(2865336225, 920715055)

# # Decrypt the provided data
# decrypted_data = encryption.decrypt_data(data)
# poke = Pokemon.from_bytes(data)
# print(poke)

print(str_to_bytes("l"))
print(bytes_to_str(b'\xEC'))
byte_sequence = b'\xEC'
string_value = byte_sequence.decode()  # or any other encoding you are using
print(string_value)