import socket
import os

def send_file(file_path, host='127.0.0.1', port=65432):
    if not os.path.exists(file_path):
        print(f"Error: File {file_path} does not exist")
        return

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((host, port))
        print(f"Connected to {host}:{port}")

        # Send file
        with open(file_path, 'rb') as f:
            while True:
                data = f.read(1024)
                if not data:
                    break
                client_socket.sendall(data)
        print(f"File {file_path} sent successfully")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        client_socket.close()

if __name__ == "__main__":
    file_to_send = input("Enter path to file (e.g., test.txt.enc): ")
    send_file(file_to_send)
