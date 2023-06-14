import socket
import threading
import pickle
import time

HOST = ''
PORT = 8080
MSG_SIZE = 8192
TIMEOUT = 100

client_dict = {} # key: name, value: (socket, addr)
passive_list = [] # List of clients who are waiting for opponent
match_list = [] # Use tuple to represent a match

def handle_match(client1, client2, client1_name, client2_name, first_macth):
    if first_macth:
        first, second = client1, client2
    else:
        first, second = client2, client1

    first.sendall("Black".encode('utf-8'))
    second.sendall("White".encode('utf-8'))
    while True:
        # Receive move from first player
        try:
            move = first.recv(MSG_SIZE).decode('utf-8')
        except TimeoutError:
            print(f'{client1_name} timeout')
            break
        if move == 'END':
            break
        second.sendall(move.encode('utf-8'))
        # Receive move from second player
        try:
            move = second.recv(MSG_SIZE).decode('utf-8')
        except TimeoutError:
            print(f'{client2_name} timeout')
            break
        
        if move == 'END':
            break
        first.sendall(move.encode('utf-8'))
    



def handle_client(client_conn, client_addr):
    global client_dict, match_list
    client_name = client_conn.recv(MSG_SIZE).decode('utf-8')

    if client_name in client_dict:
        client_conn.sendall('Name already exists'.encode('utf-8'))
        client_conn.close()
        return
    
    client_dict[client_name] = (client_conn, client_addr)
    mode = client_conn.recv(MSG_SIZE).decode('utf-8')
    print(f'Client {client_name} connected')

    if mode == "passive":
        client_conn.sendall('Connected'.encode('utf-8'))
        passive_list.append(client_name)
        time.sleep(1000000)
    elif mode == "active":
        client_conn.sendall('Connected'.encode('utf-8'))
        client_conn.sendall(pickle.dumps(passive_list))
        while True:
            opponent = client_conn.recv(MSG_SIZE).decode('utf-8')
            if opponent not in passive_list:
                client_conn.sendall('This user not available'.encode('utf-8'))
            else:
                print(f'{client_name} wants to play with {opponent}')
                client_conn.sendall('Waiting for opponent'.encode('utf-8'))
                client_dict[opponent][0].sendall(f'req {client_name} wants to play with you'.encode('utf-8'))
                confirm = client_dict[opponent][0].recv(MSG_SIZE).decode('utf-8')
                if confirm == 'OK':
                    passive_list.remove(opponent)
                    match_list.append((client_name, opponent))
                    print(f'Match between {client_name} and {opponent} started')
                    oppo_conn = client_dict[opponent][0]
                    client_conn.settimeout(TIMEOUT)
                    oppo_conn.settimeout(TIMEOUT)
                    handle_match(client_conn, oppo_conn, client_name, opponent, True)
                    print(f'Match between {client_name} and {opponent} ended')
                    break
    else:
        client_conn.sendall('Invalid mode'.encode('utf-8'))
        client_conn.close()
        return

    # Start a match
    

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    # s.setblocking(False)
    s.listen(40) # Up to 40 clients
    print("Reversi server is running...")

    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()
        