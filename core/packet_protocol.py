import json
import base64

def build_packet(
        iv: bytes, 
        ciphertext: bytes, 
        file_hash: str, 
        signature: bytes,
        key_mode: str, 
        encrypted_aes_key: bytes | None = None,
        manual_key_hash: str | None = None
    ) -> bytes:
    packet = {
        "iv": base64.b64encode(iv).decode("utf-8"),
        "ciphertext": base64.b64encode(ciphertext).decode("utf-8"),
        "file_hash": file_hash,
        "signature": base64.b64encode(signature).decode("utf-8"),
        "key_mode": key_mode,
        "encrypted_aes_key": (base64.b64encode(encrypted_aes_key).decode("utf-8")
        if encrypted_aes_key is not None
        else None
        ),
        "manual_key_hash": manual_key_hash,
    }
   
    return json.dumps(packet).encode()

def parse_packet(packet: bytes):
    data = json.loads(packet.decode("utf-8"))
    iv = base64.b64decode(data["iv"])
    ciphertext = base64.b64decode(data["ciphertext"])
    file_hash = data["file_hash"]
    signature = base64.b64decode(data["signature"])
    key_mode = data["key_mode"]
    manual_key_hash = data["manual_key_hash"]
    encrypted_aes_key = None

    if data["encrypted_aes_key"] is not None:
        encrypted_aes_key = base64.b64decode(data["encrypted_aes_key"])
    return iv, ciphertext, file_hash, signature, key_mode, encrypted_aes_key, manual_key_hash