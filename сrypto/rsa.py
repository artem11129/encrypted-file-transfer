from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes

def  generate_rsa_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
    public_key = private_key.public_key()
    return private_key, public_key  


def save_private_key(private_key, filename: str):
    pem = private_key.private_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PrivateFormat.PKCS8,
        encryption_algorithm = serialization.NoEncryption()
    )
    with open(filename, "wb") as f:
        f.write(pem)

def save_public_key(public_key, filename: str):
    pem = public_key.public_bytes(
        encoding = serialization.Encoding.PEM,
        format = serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, "wb") as f:
        f.write(pem)


def load_private_key(filename: str,):
    with open(filename, "rb") as f:
        key_data = f.read()
    
    private_key = serialization.load_pem_private_key(key_data, password=None)
    return private_key

def load_public_key(filename: str):
    with open(filename, "rb") as f:
        key_data = f.read()
    
    public_key = serialization.load_pem_public_key(key_data)
    return public_key


def encrypt_aes_key_with_rsa(aes_key: bytes, public_key):
    encrypted_key = public_key.encrypt(
        aes_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label = None
        )
    )
    return encrypted_key

def decrypt_aes_key_with_rsa(encrypted_key: bytes, private_key):
    decrypted_key = private_key.decrypt(
        encrypted_key,
        padding.OAEP(
            mgf = padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label = None
        )
    )
    return decrypted_key  