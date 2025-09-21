import socket

def start_server():
    HOST = "0.0.0.0" # can be any valid IP address
    PORT = 5000

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] TCP server running on {HOST}:{PORT}")

    while True:
        conn, addr = server.accept()
        print(f"[+] Client connected: {addr}")

        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    print(f"[-] Client disconnected: {addr}")
                    break
                message = data.decode().strip()
                print(f"[{addr}] -> {message}")
            except Exception as e:
                print(f"[!] Error with {addr}: {e}")
                break

        conn.close()

if __name__ == "__main__":
    start_server()
