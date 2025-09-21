import cv2
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading
import time

cap = cv2.VideoCapture(0)

# -----------------------------
# Server 1: Camera Stream (Port 81)
# -----------------------------
class MJPEGHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/stream':
            try:
                self.send_response(200)
                self.send_header('Content-Type', 'multipart/x-mixed-replace; boundary=frame')
                self.end_headers()

                while True:
                    ret, frame = cap.read()
                    if not ret:
                        break
                    success, jpeg = cv2.imencode('.jpg', frame)
                    if not success:
                        continue
                    try:
                        self.wfile.write(b"--frame\r\n")
                        self.send_header('Content-Type', 'image/jpeg')
                        self.send_header('Content-Length', str(len(jpeg)))
                        self.end_headers()
                        self.wfile.write(jpeg.tobytes())
                        self.wfile.write(b"\r\n")
                    except:
                        break
            finally:
                pass  # No logging

def start_camera_server():
    server = HTTPServer(('0.0.0.0', 81), MJPEGHandler)
    server.serve_forever()

# -----------------------------
# Server 2: Command Server (Port 5000)
# -----------------------------
class DebugHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get('Content-Length', 0))
        _ = self.rfile.read(length)  # receive data but do nothing
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def start_debug_server():
    server = HTTPServer(('0.0.0.0', 5000), DebugHandler)
    server.serve_forever()

# -----------------------------
# Main
# -----------------------------
if __name__ == "__main__":
    t1 = threading.Thread(target=start_camera_server, daemon=True)
    t2 = threading.Thread(target=start_debug_server, daemon=True)
    t1.start()
    t2.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        cap.release()
