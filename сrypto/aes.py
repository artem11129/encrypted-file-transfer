from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from crypto.hash import get_hash

def generate_key() -> bytes:
    return os.urandom(32)

def encrypt_file(file_path: str, key: bytes) -> bytes:
    with open(file_path, "rb") as f:
        data = f.read()

    file_hash = get_hash(data)

    padder = padding.PKCS7(128).padder()
    padder_data = padder.update(data) + padder.finalize()

    iv = os.urandom(16)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padder_data) + encryptor.finalize()
    return iv + ciphertext + file_hash.encode()

def decrypt_file(encrypted_data: bytes, key: bytes) -> bytes:
    iv = encrypted_data[:16]
    ciphertext = encrypted_data[16:-64]
    file_hash = encrypted_data[-64:].decode()

    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    if get_hash(data) != file_hash:
        print("The file may be corrupted.")
        
    return data

