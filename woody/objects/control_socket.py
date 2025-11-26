import socket
import json
import threading

class ControlSocket():
    
    def __init__(self):
        self.server_socket = None
        self.is_running = False
        
        self.local_address = "127.0.0.1"
        self.port = 6001
    
    def start_control_server(self, app):
        if self.is_running:
            return
        
        try:
            t = threading.Thread(target=self._control_server_loop, args=(app,), daemon=True)
            t.start()
        except Exception as e:
            print(f"Failed to start control server: {e}")
    
    def _control_server_loop(self, app):
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            self.server_socket.bind((self.local_address, self.port))
            self.server_socket.listen(5)
            self.is_running = True
        except Exception as e:
            print(f"Failed to bind control server: {e}")
            try:
                self.server_socket.close()
            except Exception as e:
                print(f"Failed to close server socket: {e}")
            return

        while self.is_running:
            try:
                conn, addr = self.server_socket.accept()
                data = conn.recv(4096)
                
                try:
                    msg = json.loads(data.decode("utf8"))
                except Exception:
                    conn.sendall(b'{"status":"error","message":"invalid json"}')
                    conn.close()
                    continue

                cmd = msg.get("command")
                if cmd == "show_dcc_gui":
                    port = msg.get("port", 5000)
                    app.mainWindow.after(0, lambda: app.show_or_create_dcc_gui(port))
                    conn.sendall(b'{"status":"ok"}')
                else:
                    conn.sendall(b'{"status":"error","message":"unknown command"}')

                conn.close()
            except Exception:
                if not self.is_running:
                    break
                continue
    