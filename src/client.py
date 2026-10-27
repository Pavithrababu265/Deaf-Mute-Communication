import socket
import threading
import json
import time

class NetworkClient:
    def __init__(self, host='127.0.0.1', port=5555):
        self.host = host
        self.port = port
        self.client_socket = None
        self.connected = False
        self.receive_callback = None
        self.recv_thread = None

    def connect(self, callback):
        self.receive_callback = callback
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.client_socket.connect((self.host, self.port))
            self.connected = True
            
            self.recv_thread = threading.Thread(target=self._receive_loop)
            self.recv_thread.daemon = True
            self.recv_thread.start()
            
            print(f"[CLIENT] Connected to {self.host}:{self.port}")
            return True
        except Exception as e:
            print(f"[CLIENT] Connection Failed: {e}")
            self.connected = False
            return False

    def _receive_loop(self):
        while self.connected:
            try:
                data = self.client_socket.recv(4096)
                if not data:
                    break
                
                msg = data.decode('utf-8')
                # Try to parse JSON to ensure integrity, but pass raw string or dict to callback
                try:
                    json_data = json.loads(msg)
                    if self.receive_callback:
                        self.receive_callback(json_data)
                except json.JSONDecodeError:
                     # Handle raw strings or partial packets (simple implementation assumes full packets)
                     pass
                     
            except OSError:
                break
            except Exception as e:
                print(f"[CLIENT] Receive Error: {e}")
                break
        
        self.disconnect()

    def send_message(self, data_dict):
        if not self.connected:
            return False
        
        try:
            msg = json.dumps(data_dict)
            self.client_socket.send(msg.encode('utf-8'))
            return True
        except Exception as e:
            print(f"[CLIENT] Send Error: {e}")
            self.disconnect()
            return False

    def disconnect(self):
        self.connected = False
        if self.client_socket:
            try:
                self.client_socket.close()
            except: pass
        print("[CLIENT] Disconnected")

if __name__ == "__main__":
    # Test
    def printer(data):
        print(f"Received: {data}")
    
    client = NetworkClient()
    if client.connect(printer):
        client.send_message({"msg": "Hello"})
        time.sleep(1)
        client.disconnect()
