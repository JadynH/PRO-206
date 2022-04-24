import socket
from threading import Thread

SERVER = None
IP_ADDRESS = '192.168.1.26'
PORT = 6000

CLIENTS = []


def setup():
    print("\n\t\t\t\t\t*** WELCOME TO TAMBOLA ***\n")


    global SERVER
    global PORT
    global IP_ADDRESS


    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind((IP_ADDRESS, PORT))

    SERVER.listen(10)

    print("\t\t\t\tSERVER IS WAITING FOR INCOMING CONNECTIONS...\n")


def acceptConnections():
    global CLIENTS
    global SERVER

    while True:
        player_socket, addr = SERVER.accept()
        player_name = player_socket.recv(1024).decode().strip()
        print(player_name)
        if(len(CLIENTS.keys()) == 0):
            CLIENTS[player_name] = {'player_type' : 'player1'}
        else:
            CLIENTS[player_name] = {'player_type' : 'player2'}

        
        CLIENTS[player_name]["player_socket"] = player_socket
        CLIENTS[player_name]["address"] = addr
        CLIENTS[player_name]["player_name"] = player_name
        CLIENTS[player_name]["turn"] = False

        print(f"Connection established with {player_name} : {addr}")
        


