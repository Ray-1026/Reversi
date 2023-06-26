import sys
import argparse
import random
import string
import time
import utils
import multiprocessing

from multiprocessing import Process


from gamelogic import GameLogic
from board import Board

from agent import Agent
from minimax_agent import MinimaxAgent
from alpha_zero_agent import AlphaZeroAgent
from remote_agent import RemoteAgent

from client import *

def random_name():
    return ''.join(random.choice(string.ascii_letters) for _ in range(3))

def main(args):
    PVPAgent = eval(args.agent)
    user_name = f"{args.agent}_{random_name()}"

    s = connect_server()

    name_fg = register_name(user_name, 'passive', s)
    while name_fg == 'Name already exists':
        user_name = f"{args.agent}_{random_name()}"
        name_fg = register_name(user_name, 'passive', s)
    
    if name_fg == 'Connected':
        start_sending_trash(s)
    
    while True:
        opponent = passive_recv_req(s)
        if opponent != -1:
            stop_sending_trash()
            break
    print(opponent)
    while True:
        passive_send_ok(s, user_name, opponent)
        game_order = get_game_order(s, True, True)
        if game_order != -1:
            s.sendall(packing(["OK", user_name]))
            while True:
                data = s.recv(1024).decode('utf-8')
                print("start game 1", data)
                if data == "OK":
                    break
            break
        
    print(game_order, "game_order")
    time.sleep(0.5)
    s.sendall(packing(["OK", user_name]))
    # Start PVP Game 1
    agent1 = PVPAgent(game_order)
    agent2 = RemoteAgent("white" if game_order == "black" else "black")
    game = GameLogic(agent1, agent2, None, s, user_name)
    time.sleep(0.25)
    disconnect_fg = game.run(None, None)
    if disconnect_fg == 'running_disconnect':
        print("running_disconnect")
        running_disconnect(s, user_name)
        exit(1)
    
    score = utils.getScore(game.board.board)
    s.sendall(packing(["END1", user_name, str(score[game_order]), str(score["white" if game_order == "black" else "black"])]))
    while True:
        game_order = get_game_order(s, False, True)
        if game_order != -1:
            break
    print(game_order, "game_order")
    print(user_name)
    time.sleep(2)
    s.sendall(packing(["OK", user_name]))
    while True:
        data = s.recv(1024).decode('utf-8')
        print("start game 2", data)
        if data != "OK":
            print("error")
            running_disconnect(s, user_name)
            exit(1)
        else:
            break
    time.sleep(1)
    agent1 = PVPAgent(game_order)
    agent2 = RemoteAgent("white" if game_order == "black" else "black")
    game = GameLogic(agent1, agent2, None, s, user_name)
    disconnect_fg = game.run(None, None)
    if disconnect_fg == 'running_disconnect':
        print("running_disconnect")
        running_disconnect(s, user_name)
        exit(1)
    elif disconnect_fg == 'end game':
        score = utils.getScore(game.board.board)
        s.sendall(packing(["END2", user_name, str(score[game_order]), str(score["white" if game_order == "black" else "black"])]))
        data = s.recv(2048)
        results = pickle.loads(data)
        disconnect(s)

    print("end game")
    print(results)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--agent', type=str, default='Agent')
    parser.add_argument('--num_agent', type=int, default=1)
    args = parser.parse_args()
    pool = multiprocessing.Pool(4)
    for _ in range(args.num_agent):
        pool.apply_async(main, args=(args,))


    while True:
        if pool._processes < args.num_agent:
            pool.apply_async(main, args=(args,))
            print(pool._processes)
