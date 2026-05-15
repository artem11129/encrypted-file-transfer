import hashlib
import os

from crypto.rsa import (
    generate_rsa_keys,
    save_private_key,
    save_public_key,
    load_private_key,
    load_public_key
)


def get_aes_key(mode: str) -> bytes:
    if mode == "g":
        return os.urandom(32)

    elif mode == "m":
        key_input = input("Enter AES key up to 32 characters: ")

        if len(key_input.encode()) > 32:
            raise ValueError("Key too long! Max 32 characters.")

        return hashlib.sha256(key_input.encode()).digest()

    
def ensure_rsa_keys(private_key_path: str, public_key_path: str):
    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
         private_key = load_private_key(private_key_path)
         public_key = load_public_key(public_key_path)
         return private_key, public_key

    private_key, public_key = generate_rsa_keys()

    save_private_key(private_key, private_key_path)
    save_public_key(public_key, public_key_path)

    return private_key, public_key


def derive_aes_key_from_password(password: str) -> bytes:
    return hashlib.sha256(password.encode("utf-8")).digest()


def get_manual_key_hash(password: str) -> str:
    return hashlib.sha256(password.encode("utf-8")).hexdigest()


def get_manual_aes_key_and_hash():
    key_input = input("Enter AES key up to 32 characters: ")

    if len(key_input.encode("utf-8")) > 32:
        raise ValueError("Key too long! Max 32 bytes.")

    aes_key = derive_aes_key_from_password(key_input)
    key_hash = get_manual_key_hash(key_input)

    return aes_key, key_hash 

