from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
import os
from crypto.hash import get_hash


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
    return iv, ciphertext, file_hash

def decrypt_file(iv: bytes, ciphertext: bytes, file_hash: str, key: bytes) -> tuple[bytes, bool]:
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()

    padded_data = decryptor.update(ciphertext) + decryptor.finalize()

    unpadder = padding.PKCS7(128).unpadder()
    data = unpadder.update(padded_data) + unpadder.finalize()

    hash_test = get_hash(data) == file_hash

    return data, hash_test

