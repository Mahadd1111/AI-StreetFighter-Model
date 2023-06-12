import socket
import json
import pandas as pd
from game_state import GameState
#from bot import fight
import sys
from bot import Bot
def connect(port):
    #For making a connection with the game
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print ("Connected to game!")
    return client_socket

def send(client_socket, command):
    #This function will send your updated command to Bizhawk so that game reacts according to your command.
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    #receive the game state and return game state
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)

    return game_state

def main():
    if (sys.argv[1]=='1'):
        client_socket = connect(9999)
    elif (sys.argv[1]=='2'):
        client_socket = connect(10000)
    current_game_state = None
    #print( current_game_state.is_round_over )
    bot=Bot()
    buffer = []
    game_mode = "BOT_TESTING"
    # game_mode = "AI_TRAINING"
    while (current_game_state is None) or (not current_game_state.is_round_over):
        # Player 1 is the bot , Player 2 is the human
        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state,sys.argv[1])
        player1 = current_game_state.player1
        player2 = current_game_state.player2
        p1buttons = current_game_state.player1.player_buttons
        p2buttons = current_game_state.player2.player_buttons
        print("------------------------------------------")
        print(f"DATA P1 : ID {player1.player_id} | HP : {player1.health} | (X,Y) : ({player1.x_coord},{player1.y_coord}) | isMove : {player1.is_player_in_move} | moveID: {player1.move_id}| jump: {player1.is_jumping} | crouching: {player1.is_crouching}")
        print(f"DATA P2 : ID {player2.player_id} | HP : {player2.health} | (X,Y) : ({player2.x_coord},{player2.y_coord}) | isMove : {player2.is_player_in_move} | moveID: {player2.move_id}| jump: {player2.is_jumping} | crouching: {player2.is_crouching}")
        print(f"DATA P2 : Buttons -> A: {p2buttons.A} | B: {p2buttons.B} | R: {p2buttons.R} | L: {p2buttons.L} | Y : {p2buttons.Y} | X: {p2buttons.X} | Left : {p2buttons.left} | Right {p2buttons.right} | Down: {p2buttons.down} | Up: {p2buttons.up}")
        if game_mode=="AI_TRAINING":
            data_instance = {
                'timer': current_game_state.timer, 'result': current_game_state.fight_result, 'round_over': current_game_state.is_round_over,
                'p1_id': player1.player_id, 'p1_hp': player1.health, 'p1_xc': player1.x_coord, 'p1_yc': player1.y_coord, 'p1_ismove': player1.is_player_in_move, 'p1_moveid': player1.move_id,
                'p1_isjump': player1.is_jumping, 'p1_iscrouch': player1.is_crouching,
                'p2_id': player2.player_id, 'p2_hp': player2.health, 'p2_xc': player2.x_coord, 'p2_yc': player2.y_coord, 'p2_ismove': player2.is_player_in_move, 'p2_moveid': player2.move_id,
                'p2_isjump': player2.is_jumping, 'p2_iscrouch': player2.is_crouching,
                'p1btnA': p1buttons.A, 'p1btnB': p1buttons.B, 'p1btnR': p1buttons.R, 'p1btnL': p1buttons.L, 'p1btnY': p1buttons.Y, 'p1btnX': p1buttons.X, 'p1btnLeft': p1buttons.left,
                'p1btnRight': p1buttons.right, 'p1btnUp': p1buttons.up, 'p1btnDown': p1buttons.down,
                'p2btnA': p2buttons.A, 'p2btnB': p2buttons.B, 'p2btnR': p2buttons.R, 'p2btnL': p2buttons.L, 'p2btnY': p2buttons.Y, 'p2btnX': p2buttons.X, 'p2btnLeft': p2buttons.left,
                'p2btnRight': p2buttons.right, 'p2btnUp': p2buttons.up, 'p2btnDown': p2buttons.down
            }
            buffer.append(data_instance)
            if len(buffer) == 50:
                with open('dataset.csv', mode='a', newline='') as file:
                    pd.DataFrame(buffer).to_csv(file, header=file.tell() == 0, index=False)
                buffer = []
        send(client_socket, bot_command)
    if buffer and game_mode=="AI_TRAINING":
        with open('dataset.csv',mode='a',newline='') as file:
            pd.DataFrame(buffer).to_csv(file, header=file.tell() == 0, index=False)
if __name__ == '__main__':
   main()
