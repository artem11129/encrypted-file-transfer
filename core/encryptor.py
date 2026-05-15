from crypto.aes import encrypt_file
from crypto.rsa import encrypt_aes_key_with_rsa
from crypto.signature import sign_data
from core.packet_protocol import build_packet


def encrypt_and_package(file_path: str, 
                        aes_key: bytes, 
                        private_key, 
                        public_key, 
                        key_mode: str, 
                        manual_key_hash: str | None = None
                    ) -> bytes:
    iv, ciphertext, file_hash = encrypt_file(file_path, aes_key)
    signature = sign_data(ciphertext, private_key)
    encrypted_aes_key = None
    if key_mode == "g":
        encrypted_aes_key = encrypt_aes_key_with_rsa(aes_key, public_key)
    
    packet = build_packet(iv, ciphertext, file_hash, signature, key_mode, encrypted_aes_key, manual_key_hash)
    return packet