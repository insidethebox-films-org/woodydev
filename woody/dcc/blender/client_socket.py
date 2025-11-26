import socket
import json

HOST = "127.0.0.1"

def execute_operation(operation, port=5000, args=None, on_success=None, on_error=None):
    if args is None:
        args = {}
    
    msg = {
        "operation": operation,
        "args": args
    }
    
    try:
        s = socket.create_connection((HOST, port), timeout=5)
        s.sendall(json.dumps(msg).encode())
        response = json.loads(s.recv(4096).decode())
        s.close()
        
        if response.get("status") == "ok":
            if on_success:
                on_success(response.get("result"))
        else:
            if on_error:
                on_error(response.get("message"))
        
        return response
        
    except Exception as e:
        if on_error:
            on_error(str(e))
        return {"status": "error", "message": str(e)}
    