import os
import socket
import json
import hou

HOST = "127.0.0.1"

def execute_operation(operation, args=None, on_success=None, on_error=None):
    port = int(os.environ.get("HOUDINI_TOOL_PORT", 5000))
    
    hou.ui.setStatusMessage(
        f"[Woody] Executing operation: {operation} on port {port}"
    )
    
    if args is None:
        args = {}
    
    msg = {
        "command": operation,
        "args": args
    }
    
    try:
        s = socket.create_connection((HOST, port), timeout=5)
        s.sendall(json.dumps(msg).encode())
        
        response_data = s.recv(8192).decode()
        
        if not response_data:
            raise ValueError("No response from server.")
            
        response = json.loads(response_data)
        s.close()
        
        if response.get("status") == "ok":
            result = response.get("result")
            if on_success:
                on_success(result)
            return response
        else:
            msg = response.get("message", "Unknown error")
            if on_error:
                on_error(msg)
            return response
            
    except Exception as e:
        print(f"[Woody] Error: {e}")
        if on_error:
            on_error(str(e))
        return {"status": "error", "message": str(e)}