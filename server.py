import socket
import os

def start_server(host='127.0.0.1', port=65432):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(1)
    print(f"Server listening on {host}:{port}")

    conn, addr = server_socket.accept()
    with conn:
        print(f"Connected by {addr}")
        # Receive file
        with open('received_file.enc', 'wb') as f:
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                f.write(data)
        print("File received: received_file.enc")

if __name__ == "__main__":
    start_server()
