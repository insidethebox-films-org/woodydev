import socket

def get_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as tmp:
        tmp.bind(('', 0)) 
        return tmp.getsockname()[1]