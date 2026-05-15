# Encrypted File Transfer System

## About The Project

Encrypted File Transfer System is a secure client-server application written in Python for encrypted file transmission over a TCP network connection.

This project was developed as a student educational project in the field of computer networks and cybersecurity. The main task was to create a client-server application that allows encrypted file transfer, key exchange, file integrity verification, and digital signature validation.

The purpose of the project was to demonstrate the practical use of modern cryptographic methods in a real network application.

The system implements:

- AES-256 symmetric encryption for file encryption;
- RSA-2048 encryption for secure AES key exchange;
- RSA digital signatures for sender authenticity verification;
- SHA-256 hashing for file integrity checking;
- chunk-based file transfer for supporting files of different sizes and formats.

The application allows the client to encrypt a file, protect the session key using the server’s public RSA key, sign the file, and send it to the server over TCP. After receiving the file, the server can decrypt it, verify its integrity, and check the digital signature.

Overall, this project demonstrates how hybrid cryptography, encrypted key exchange, digital signatures, and integrity verification can be combined in one student-level secure file transfer system.

---

# What This Project Does

The application performs the following operations:

## 1. File Encryption
The client encrypts a file using:
- AES-256
- CBC mode
- PKCS7 padding
- random IV generation

---

## 2. AES Key Protection
If automatic mode is selected:
- a random AES key is generated,
- the AES key is encrypted using RSA-2048 public key encryption,
- the encrypted AES key is sent securely to the server.

---

## 3. Manual AES Mode
If manual mode is selected:
- the user enters a custom AES password,
- SHA-256 derives a valid AES-256 key,
- the server requests the same password before decryption,
- password hashes are compared for verification.

---

## 4. Digital Signature
The encrypted file is digitally signed using:
- RSA-PSS
- SHA-256

The server verifies the signature to confirm:
- authenticity,
- integrity,
- and sender verification.

---

## 5. File Transfer
The encrypted packet is transferred:
- through TCP sockets,
- in 4096-byte chunks,
- with support for large files.

---

## 6. Integrity Verification
After decryption:
- SHA-256 hash is recalculated,
- the server compares hashes,
- the system confirms whether the file remained unchanged during transmission.

---

# Project Architecture

```
project/
│
├── core/
│   ├── encryptor.py
│   ├── keys_manager.py
│   └── packet_protocol.py
│
├── crypto/
│   ├── aes.py
│   ├── hash.py
│   ├── rsa.py
│   └── signature.py
│
├── network/
│   ├── client.py
│   └── server.py
│
├── files/
│   ├── client_files/
│   └── server_files/
│
├── private.pem
├── public.pem
├── requirements.txt
└── README.md
```

---

# Architecture Explanation

## crypto/

Contains all cryptographic functionality:
- AES encryption/decryption
- RSA key generation and encryption
- SHA-256 hashing
- Digital signatures

---

## core/

Contains application logic:
- packet creation/parsing
- AES key management
- encryption packaging logic

---

## network/

Contains networking logic:
- TCP client
- TCP server
- chunk transfer
- connection handling

---

## files/

### client_files/
Contains files that the client sends.

### server_files/
Contains:
- received encrypted packets,
- decrypted files.

---

# How The Encryption Process Works

## Client Side

```text
File
↓
SHA-256 Hash
↓
AES-256 Encryption
↓
Ciphertext
↓
RSA Digital Signature
↓
Packet Creation
↓
TCP Chunk Transfer
```

---

## Server Side

```text
Receive Packet
↓
Parse Packet
↓
Verify Signature
↓
Decrypt AES Key
↓
AES Decryption
↓
Integrity Verification
↓
Save File
```

---

# Technologies Used

- Python 3
- TCP Sockets
- AES-256
- RSA-2048
- SHA-256
- RSA-PSS
- OAEP Padding
- PKCS7 Padding
- cryptography library

---

# How To Use

# 1. Clone Repository

```bash
git clone https://github.com/artem11129/encrypted-file-transfer.git
cd encrypted-file-transfer
```

---

# 2. Create Virtual Environment

## Windows PowerShell

```bash
py -m venv venv
.\venv\Scripts\Activate.ps1
```

---

# 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# 4. Start Server

```bash
py -m network.server
```

---

# 5. Start Client

Open a second terminal:

```bash
py -m network.client
```

---

# Client Commands

## Send File

```text
send data.txt
```

Example:

```text
send stress_50mb.txt
```

Files are loaded from:


---

## Exit Client

```text
exit
```

---

# Example Transfer Report

```text
========== FILE TRANSFER REPORT ==========
Client address: ('127.0.0.1', 53421)
Packet size: 52428800 bytes
Received bytes: 52428800 bytes
Chunks received: 12800
Ciphertext size: 52428784 bytes
Decrypted file size: 52428768 bytes
Key mode: g
SHA-256 hash: 8d3f...
Integrity valid: True
Signature valid: True
Output file: files/server_files/decrypted_file.txt
==========================================
```

---

# Security Features

- AES-256 file encryption
- RSA-2048 key exchange
- OAEP secure padding
- RSA-PSS digital signatures
- SHA-256 integrity verification
- Random IV generation
- Password-derived AES keys
- Binary-safe file transfer

---

# Current Limitations

- Entire packet is temporarily stored in RAM before parsing
- Shared RSA key pair between client and server
- Single-client server architecture
- No TLS transport layer

---


# Author

Artem Nakonechyy

GitHub:
https://github.com/artem11129