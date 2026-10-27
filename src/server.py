import socket
import threading
import json
import sys

class CommunicationServer:
    def __init__(self, host='0.0.0.0', port=5555):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.running = False

    def start(self):
        try:
            self.server_socket.bind((self.host, self.port))
            self.server_socket.listen(5)
            self.running = True
            print(f"[SERVER] Listening on {self.host}:{self.port}")
            
            while self.running:
                client_socket, address = self.server_socket.accept()
                print(f"[SERVER] Connection from {address}")
                self.clients.append(client_socket)
                threading.Thread(target=self.handle_client, args=(client_socket,)).start()
        except Exception as e:
            print(f"[SERVER] Error: {e}")
        finally:
            self.stop()

    def handle_client(self, client_socket):
        try:
            while self.running:
                data = client_socket.recv(4096)
                if not data:
                    break
                
                # Broadcast message to all other clients
                # Ideally we check JSON validity, but for speed we just relay bytes
                # Or decode -> print -> encode -> broadcast
                try:
                    msg = data.decode('utf-8')
                    print(f"[RELAY] {msg}")
                    self.broadcast(msg, client_socket)
                except:
                    pass

        except Exception as e:
            print(f"[SERVER] Client Error: {e}")
        finally:
            self.remove_client(client_socket)

    def broadcast(self, message, sender_socket):
        for client in self.clients:
            if client != sender_socket:
                try:
                    client.send(message.encode('utf-8'))
                except:
                    self.remove_client(client)

    def remove_client(self, client_socket):
        if client_socket in self.clients:
            self.clients.remove(client_socket)
            try:
                client_socket.close()
            except: pass
        print(f"[SERVER] Client Disconnected. Total: {len(self.clients)}")

    def stop(self):
        self.running = False
        try:
            self.server_socket.close()
        except: pass
        sys.exit(0)

if __name__ == "__main__":
    server = CommunicationServer()
    server.start()
