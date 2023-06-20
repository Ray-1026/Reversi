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
    online_list = s.recv(8192)
    
    return pickle.loads(online_list) 

def send_opponent(s, opponent):
    s.sendall(opponent.encode())
    s.sendall(opponent.encode())
    try:
        data = s.recv(8192).decode('utf-8')
    except:
        return -1
    return data

def passive_recv_req(s):
    data = s.recv(8192).decode('utf-8')
    return data[4:] if data.startswith('req') else -1

def active_req_ok(s):
    data = s.recv(8192).decode('utf-8')
    return data == 'OK'

def passive_send_ok(s):
    s.sendall('OK'.encode())
    
def get_game_order(s):
    data = s.recv(8159).decode('utf-8')
    print(data)
    if 'white' in data or 'black' in data:
        return data
    else:
        return -1

def disconnect(s):
    s.sendall('disconnect'.encode())
    s.close()