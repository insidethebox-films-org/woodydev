import socket
import json
import traceback

HOST = "127.0.0.1"

def run_server(port, processor):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind((HOST, port)) 
        s.listen()
        print(f"[Woody] Listening on PORT: {port}")

        while True:
            conn, addr = s.accept()
            with conn:
                try:
                    data = conn.recv(8192).decode()
                    if not data: 
                        continue
                    
                    req = json.loads(data)
                    cmd = req.get("command")
                    args = req.get("args", {})

                    if "." in cmd:
                        parts = cmd.split(".")
                        obj = processor
                        for part in parts[:-1]:
                            obj = getattr(obj, part)
                        func = getattr(obj, parts[-1])
                    else:
                        func = getattr(processor, cmd, None)
                    
                    if func and callable(func):
                        result = func(**args)
                        response = {"status": "ok", "result": result}
                    else:
                        response = {"status": "error", "message": f"Method {cmd} not found on {type(processor).__name__}"}
                        
                except Exception as e:
                    print(f"[Woody] Error: {traceback.format_exc()}")
                    response = {"status": "error", "message": str(e)}

                conn.sendall(json.dumps(response).encode())