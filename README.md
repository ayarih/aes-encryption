# aes-encryption

# File Encryption & Transfer Tool

A secure file encryption application with network transfer capabilities, built with Python and GTK4. This tool provides AES-256 encryption with a modern graphical interface and command-line network utilities.

## Features

- **AES-256 Encryption**: Industry-standard encryption with CBC mode
- **Modern GUI**: Built with GTK4 and Libadwaita for a native Linux experience
- **Key Management**: Generate secure random keys or use custom keys
- **Network Transfer**: Simple client-server architecture for encrypted file sharing
- **File Integrity**: Proper padding and IV handling for secure encryption

## Components

### 1. Encryption GUI (`encrypt_decrypt.py`)
The main application provides a user-friendly interface for:
- Selecting files to encrypt/decrypt
- Generating secure 256-bit encryption keys
- Encrypting files with `.enc` extension
- Decrypting files with `.decrypted` extension

### 2. Network Server (`server.py`)
A simple TCP server that:
- Listens on localhost:65432 by default
- Receives encrypted files from clients
- Saves received files as `received_file.enc`

### 3. Network Client (`client.py`)
A command-line client that:
- Connects to the server
- Transfers files in 1KB chunks
- Provides transfer status feedback

## Installation

### Prerequisites
```bash
# Fedora 42
sudo dnf install python3-pip python3-gobject gtk4-devel libadwaita-devel python3-cairo-devel

# Ubuntu/Debian
sudo apt install python3 python3-pip python3-gi gir1.2-gtk-4.0 gir1.2-adw-1

# Arch Linux
sudo pacman -S python python-pip python-gobject gtk4 libadwaita
```

### Python Dependencies
```bash
pip install pycryptodome pygobject
```

## Usage

### Encrypting Files (GUI)
1. Run the encryption application:
   ```bash
   python encrypt_decrypt.py
   ```
2. Click "Select File" to choose your file
3. Either generate a new key or enter a 32-byte hex key
4. Click "Encrypt File" to create an `.enc` file

### Decrypting Files (GUI)
1. Select your encrypted `.enc` file
2. Enter the same key used for encryption
3. Click "Decrypt File" to restore the original file

### Network Transfer
1. Start the server:
   ```bash
   python server.py
   ```

2. In another terminal, run the client:
   ```bash
   python client.py
   ```

3. Enter the path to your encrypted file when prompted

## Security Features

- **AES-256-CBC**: Strong encryption with 256-bit keys
- **Random IV**: Each encryption uses a unique initialization vector
- **PKCS7 Padding**: Proper block padding for file integrity
- **Secure Key Generation**: Cryptographically secure random key generation

## File Structure

```
project/
├── encrypt_decrypt.py    # Main GUI application
├── server.py            # Network server
├── client.py           # Network client
└── README.md          # This file
```

## Network Protocol

The client-server communication uses a simple TCP protocol:
- Server listens on `127.0.0.1:65432`
- Client connects and streams file data in 1KB chunks
- Server saves the complete file as `received_file.enc`

## Example Workflow

1. **Encrypt a document**:
   - Run GUI, select `document.pdf`
   - Generate key: `a1b2c3d4e5f6...` (64 hex characters)
   - Output: `document.pdf.enc`

2. **Transfer encrypted file**:
   - Start server: `python server.py`
   - Run client: `python client.py`
   - Input: `document.pdf.enc`
   - Server receives: `received_file.enc`

3. **Decrypt on receiving end**:
   - Run GUI, select `received_file.enc`
   - Enter same key: `a1b2c3d4e5f6...`
   - Output: `received_file.enc.decrypted`

## Security Notes

⚠️ **Important**: This tool is for educational/personal use. For production systems:
- Use authenticated encryption (GCM mode)
- Implement secure key exchange protocols
- Add proper error handling and logging
- Consider using established libraries like `cryptography`

## Requirements

- Python 3.8+
- GTK 4.0+
- Libadwaita 1.0+
- PyCryptodome
- PyGObject

## Contributing

Feel free to submit issues and pull requests. Areas for improvement:
- Better error handling
- Authenticated encryption modes
- Key derivation functions
- Progress bars for large files
- Network encryption for client-server communication
