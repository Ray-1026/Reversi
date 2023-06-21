# Echo client program
import socket
import pickle
import time

HOST = '127.0.0.1'    # The remote host
PORT = 8080             # The same port as used by the server
def connect_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def register_name(name, mode, s):
    s.sendall(name.encode())
    time.sleep(0.5)    
    s.sendall(mode.encode())
    data = s.recv(1024)

    return data == b'Connected'

def request_online_list(s):
    s.sendall('online_list'.encode())
    try:
        online_list = s.recv(8192)
    except:
        return -1
    return pickle.loads(online_list) 