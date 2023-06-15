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
    if data == b'Connected':
        # s.sendall(b'OK')
        if mode == "active":
            data = s.recv(8192)
            print(pickle.loads(data))
            while True:
                oppo = input()
                s.sendall(oppo.encode('utf-8'))
                data = s.recv(8192).decode('utf-8')
                print(data)
                if data != "This user not available":
                    break
        elif mode == "passive":
            while True:
                data = s.recv(8192).decode('utf-8')
                print(data)
                if data.startswith("req"):
                    confirm = input()
                    s.sendall(confirm.encode('utf-8'))
                    break
            
        while True:
            color = s.recv(8192).decode('utf-8')
            if color == "Black" or color == "White":
                print("Start")
                break

def request_online_list(s):
    s.sendall('online_list'.encode())
    try:
        online_list = s.recv(8192)
    except:
        return -1
    return pickle.loads(online_list) 


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        name = input()
        s.sendall(name.encode())
        mode = input()
        s.sendall(mode.encode())
        data = s.recv(1024)
        if data == b'Connected':
            # s.sendall(b'OK')
            if mode == "active":
                data = s.recv(8192)
                print(pickle.loads(data))
                while True:
                    oppo = input()
                    s.sendall(oppo.encode('utf-8'))
                    data = s.recv(8192).decode('utf-8')
                    print(data)
                    if data != "This user not available":
                        break
            elif mode == "passive":
                while True:
                    data = s.recv(8192).decode('utf-8')
                    print(data)
                    if data.startswith("req"):
                        confirm = input()
                        s.sendall(confirm.encode('utf-8'))
                        break
                
            while True:
                color = s.recv(8192).decode('utf-8')
                print(color)
                if color == "Black" or color == "White":
                    print("Start")
                    break
    
            while True:
                if color == "Black":
                    print("Black")
                    move = input()
                    print(f"Sending {move}")
                    s.sendall(move.encode('utf-8'))
                    data = s.recv(8192).decode('utf-8')
                    print(data)
                    if data == "END":
                        break
                elif color == "White":
                    print("White")
                    data = s.recv(8192).decode('utf-8')
                    print(data)
                    move = input()
                    print(f"Sending {move}")
                    s.sendall(move.encode('utf-8'))
                    if data == "END":
                        break
                else:
                    print("?")
        else:
            print(pickle.load(data))