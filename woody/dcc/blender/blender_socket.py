import bpy
import socket
import threading
import json
import os
import sys
import queue
import random

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.append(SCRIPT_DIR)

from operations import OPERATIONS

HOST = "127.0.0.1"
PORT = random.choice([p for p in range(1024, 49152) if p != 6001])

# Store PORT in window manager for addon access
bpy.context.window_manager["woody_socket_port"] = PORT

operation_queue = queue.Queue()

def run_operation(data):
    try:
        op = data.get("operation")
        args = data.get("args", {})

        if op not in OPERATIONS:
            return {"status": "error", "message": f"Unknown operation '{op}'"}

        fn = OPERATIONS[op]
        result = fn(**args)
        return {"status": "ok", "result": result}

    except Exception as e:
        return {"status": "error", "message": str(e)}

def process_operations():
    try:
        if not operation_queue.empty():
            data, result_queue = operation_queue.get_nowait()
            result = run_operation(data)
            result_queue.put(result)
    except:
        pass
    return 0.01

def socket_loop():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(5)

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(8192)

            try:
                msg = json.loads(data.decode("utf8"))
            except:
                conn.sendall(b'{"status":"error","message":"invalid json"}')
                conn.close()
                continue

            result_queue = queue.Queue()
            operation_queue.put((msg, result_queue))
            
            resp = result_queue.get(timeout=30)

            conn.sendall(json.dumps(resp).encode("utf8"))
            conn.close()
            
        except:
            break

    s.close()

threading.Thread(target=socket_loop, daemon=True).start()
bpy.app.timers.register(process_operations)