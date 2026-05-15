import os
import socket
from core.encryptor import encrypt_and_package
from core.keys_manager import ensure_rsa_keys, get_aes_key, get_manual_aes_key_and_hash

HOST = "127.0.0.1"
PORT = 5000

CLIENT_FILES_DIR = "files/client_files"

PRIVATE_KEY_PATH = "private.pem"
PUBLIC_KEY_PATH = "public.pem"

CHUNK_SIZE = 4096

EXIT_COMMANDS = ("exit","Exit", "quit", "q", "e", "close", "c", "EXIT", "QUIT", "Q", "E", "C", "CLOSE", "Close")
SEND_COMMANDS = ("send ", "Send ", "SEND ")



def choose_aes_key():
    manual_key_hash = None

    while True:
        choice = input("Generate AES key or manual? (g/m): ")
        if choice == "g":
            aes_key = get_aes_key("g")
            return aes_key, choice, manual_key_hash

        elif choice == "m":
            aes_key, manual_key_hash = get_manual_aes_key_and_hash()
            return aes_key, choice, manual_key_hash
        
        print("Invalid mode. Enter 'g' or 'm'.")


def send_packet(packet: bytes):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.connect((HOST, PORT))
    print(f"Connected to server at {HOST}:{PORT}")

    packet_size = len(packet)
    print(f"Packet size: {packet_size} bytes")

    client.sendall(packet_size.to_bytes(8, byteorder="big"))

    chunk_num = 1

    for i in range(0, packet_size, CHUNK_SIZE):
        chunk = packet[i:i + CHUNK_SIZE]

        client.sendall(chunk)

        print(f"Sent chunk {chunk_num}")

        chunk_num += 1

    print("Encrypted packet sent successfully")

    client.close()        

#-------------------Main loop-------------------#
def main():
    private_key, public_key = ensure_rsa_keys(
        PRIVATE_KEY_PATH,
        PUBLIC_KEY_PATH
    )

    while True:
        command = input("\nEnter command (send <file_path> / exit): ").strip()

        if command in EXIT_COMMANDS:
            print("Client closed.")
            exit(0)

        if not command.startswith(SEND_COMMANDS):
            print("Unknown command. Use: send <file_path> or exit")
            continue

        file_path = command[5:].strip()

        if not file_path:
            print("File path is empty.")
            continue

        if not os.path.isabs(file_path):
            file_path = os.path.join(CLIENT_FILES_DIR, file_path)

        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            continue

        aes_key, choice, manual_key_hash = choose_aes_key()
        packet = encrypt_and_package(file_path, aes_key, private_key, public_key, choice, manual_key_hash)
        send_packet(packet)

main()



