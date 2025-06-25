import base64
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes

# AES configuration
BLOCK_SIZE = 16  # AES block size in bytes

def aes_encrypt_text(plain_text, key):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes.ljust(32, b'\x00')[:32]  # pad or trim key to 32 bytes for AES-256
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), BLOCK_SIZE))
    iv = base64.b64encode(cipher.iv).decode('utf-8')
    ct = base64.b64encode(ct_bytes).decode('utf-8')
    return iv + ":" + ct

def aes_decrypt_text(cipher_text, key):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes.ljust(32, b'\x00')[:32]
    iv, ct = cipher_text.split(":")
    iv = base64.b64decode(iv)
    ct = base64.b64decode(ct)
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), BLOCK_SIZE)
    return pt.decode('utf-8')

def aes_encrypt_image(pixel_array, key):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes.ljust(32, b'\x00')[:32]
    cipher = AES.new(key_bytes, AES.MODE_CBC)
    # Convert pixel array (list of ints) to bytes
    pixel_bytes = bytes(pixel_array)
    ct_bytes = cipher.encrypt(pad(pixel_bytes, BLOCK_SIZE))
    iv = cipher.iv
    # Return iv + ciphertext as list of ints
    encrypted_bytes = iv + ct_bytes
    return list(encrypted_bytes)

def aes_decrypt_image(encrypted_array, key):
    key_bytes = key.encode('utf-8')
    key_bytes = key_bytes.ljust(32, b'\x00')[:32]
    encrypted_bytes = bytes(encrypted_array)
    iv = encrypted_bytes[:BLOCK_SIZE]
    ct_bytes = encrypted_bytes[BLOCK_SIZE:]
    cipher = AES.new(key_bytes, AES.MODE_CBC, iv)
    pt_bytes = unpad(cipher.decrypt(ct_bytes), BLOCK_SIZE)
    return list(pt_bytes)


# Vigenere example
def vigenere_encrypt(plain_text, key):
    plain_text = plain_text.replace(" ", "").lower()
    key = key.lower()

    cipher_text = ""

    pt_chars = list(plain_text)
    key_chars = list(key)

    curr_key_index = 0

    for curr_pt_char in pt_chars:
        curr_ct_char = (char_to_num(curr_pt_char) + char_to_num(key_chars[curr_key_index])) % 26
        curr_key_index = (curr_key_index + 1) % len(key_chars)
        cipher_text += num_to_char(curr_ct_char)
        
    return (cipher_text)

def vigenere_decrypt(cipher_text, key):
    key = key.lower()

    plain_text = ""

    ct_chars = list(cipher_text)
    key_chars = list(key)

    curr_key_index = 0

    for curr_ct_char in ct_chars:
        curr_pt_char = (char_to_num(curr_ct_char) - char_to_num(key_chars[curr_key_index]) + 26) % 26
        curr_key_index = (curr_key_index + 1) % len(key_chars)
        plain_text += num_to_char(curr_pt_char)
        
    return (plain_text)

def char_to_num(char):
    return ord(char) - ord('a')

def num_to_char(num):
    return chr((num) + ord('a'))

def image_vigenere_encrypt(pixel_array, key):
    key_nums = [ord(c) for c in key]
    key_len = len(key_nums)
    encrypted = []
    for i in range(len(pixel_array)):
        encrypted_value = (pixel_array[i] + key_nums[i % key_len] * key_nums[i % key_len]) % 256
        encrypted.append(encrypted_value)
    return encrypted
