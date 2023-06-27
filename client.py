# Echo client program
import socket
import pickle
import time
from threading import Event, Thread

SLEEP_TIME = 0.5
SLEEP_TIME = 0.5
event = Event()
# HOST = 'reversi.jayinnn.dev'    # The remote host
HOST = 'localhost'
PORT = 8080             # The same port as used by the server

def packing(things: list):
    return '#'.join(things).encode('utf-8')
    

def connect_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    return s

def register_name(name, mode, s):
    content = packing(['register', name, mode])
    s.sendall(content)
    data = s.recv(1024).decode('utf-8')
    return data

def request_online_list(s):
    content = packing(['online_list'])
    s.sendall(content)
    online_list = s.recv(8192)
    
    return pickle.loads(online_list) 

def send_opponent(s, user_name, opponent):
    content = packing(['active_req', user_name, opponent])
    s.sendall(content)

def passive_recv_req(s):
    data = s.recv(8192).decode('utf-8')
    return data[4:] if data.startswith('req') else -1


def active_req_ok(s):
    data = s.recv(8192).decode('utf-8')
    return data

def passive_send_ok(s, name, opponent):
    content = packing(['passive_confirm', name, opponent])
    s.sendall(content)
    data = s.recv(1024).decode('utf-8')
    print(data)
    return data
    
    
def get_game_order(s, first_game, passive):
    game_cnt = 'first' if first_game else 'second'
    mode = 'passive' if passive else 'active'
    content = packing(['game_order', game_cnt, mode])
    s.sendall(content)
    data = s.recv(1024).decode('utf-8')
    print(data, "receive")
    if 'white' == data or 'black' == data:
        return data
    else:
        return -1

def disconnect(s, user_name=None):
    if user_name:
        content = packing(['disconnect', user_name])
    else:
        content = packing(['disconnect'])
    s.sendall(content)
    if not event.is_set():
        stop_sending_trash(s)
    
def sending_trash(s, event):
    while True:
        if event.is_set():
            break
        else:
            time.sleep(SLEEP_TIME)
            s.sendall('no_event'.encode())

def start_sending_trash(s):
    event.clear()
    Thread(target=sending_trash, args=(s, event)).start()
def stop_sending_trash(s):
    event.set()
    data = s.recv(1024)

def send_move(s, move: list, user_name):
    content = packing(['play', user_name, str(move[0]), str(move[1])])
    s.sendall(content)
    
def running_disconnect(s, user_name):
    content = packing(['running_disconnect', user_name])
    s.sendall(content)
