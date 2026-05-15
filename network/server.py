import socket
from core.packet_protocol import parse_packet
from crypto.rsa import load_private_key, load_public_key, decrypt_aes_key_with_rsa
from crypto.signature import verify_signature
from crypto.aes import decrypt_file
from core.keys_manager import get_manual_aes_key_and_hash


HOST = "127.0.0.1"
PORT = 5000

CHUNK_SIZE = 4096

PRIVATE_KEY_PATH = "private.pem"
PUBLIC_KEY_PATH = "public.pem"

OUTPUT_FILE = "decrypted_file.txt"

def receive_packet(conn):
    packet_size_bytes = conn.recv(8)

    if not packet_size_bytes:
        return None, 0, 0

    packet_size = int.from_bytes(packet_size_bytes, byteorder="big")

    print(f"Incoming packet size: {packet_size} bytes")

    data = b""
    chunk_count = 0

    while len(data) < packet_size:
        chunk = conn.recv(CHUNK_SIZE)

        if not chunk:
            break

        data += chunk
        chunk_count += 1

    return data, packet_size, chunk_count

def process_packet(data, packet_size, chunk_count, addr):
    iv, ciphertext, file_hash, signature, key_mode, encrypted_aes_key, manual_key_hash = parse_packet(data)
    private_key = load_private_key(PRIVATE_KEY_PATH)
    public_key = load_public_key(PUBLIC_KEY_PATH)

    signature_valid = verify_signature(
        ciphertext,
        signature,
        public_key
    )
    
    if key_mode == "g":
        aes_key = decrypt_aes_key_with_rsa(
            encrypted_aes_key,
            private_key
        )

    elif key_mode == "m":
        print("Manual AES mode detected.")

        while True:
            aes_key, server_manual_key_hash = get_manual_aes_key_and_hash()

            if server_manual_key_hash == manual_key_hash:
                print("Manual AES key verified successfully.")
                break

            print("Wrong manual AES key. Try again.")

    with open("received_data.bin", "wb") as f:
        f.write(data)

    print("Saved received data to received_data.bin")



    decrypted_file, integrity_valid = decrypt_file(
        iv,
        ciphertext,
        file_hash,
        aes_key
    )


    with open(OUTPUT_FILE, "wb") as f:
        f.write(decrypted_file)

    print("\n========== FILE TRANSFER REPORT ==========")
    print(f"Client address: {addr}")
    print(f"Packet size: {packet_size} bytes")
    print(f"Received bytes: {len(data)} bytes")
    print(f"Chunks received: {chunk_count}")
    print(f"Ciphertext size: {len(ciphertext)} bytes")
    print(f"Decrypted file size: {len(decrypted_file)} bytes")
    print(f"Key mode: {key_mode}")
    print(f"SHA-256 hash: {file_hash}")
    print(f"Integrity valid: {integrity_valid}")
    print(f"Signature valid: {signature_valid}")
    print(f"Output file: {OUTPUT_FILE}")
    print("==========================================\n")

def main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"Connected by {addr}")

        data, packet_size, chunk_count = receive_packet(conn)

        if data is None:
            conn.close()
            continue

        process_packet(data, packet_size, chunk_count, addr)

        conn.close()
        print("Connection closed. Waiting for next file...")

main()