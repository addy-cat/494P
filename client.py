#!/usr/bin/env python3
import socket
import json
import threading

IP = '0.0.0.0'
PORT = 8080
CURR_ROOM = ''
def prompt(user, message):
    return input(f'{message} - {user}> ')
# Usage: print(prompt('redawl', 'Testing client side'))

def message_handler(sock, placeholder):
    while True:
        try:
            print(sock.recv(8192).decode() + f'\n{user}> ', end='')
        except:
            exit()
client = socket.socket()

client.connect((IP,PORT))
print(f'Connecting to {IP}:{PORT}')

user = input('Enter your username > ')
client.send(user.encode())
print("Welcome to server! type '/help' for info")
# Set up listener for room messages
new_thread = threading.Thread(
    group=None,
    target=message_handler,
    name=None,
    args=(client, None),
    kwargs={}
)  
new_thread.start()
command = ''
while command != '/dis':
    command = prompt(user, 'What would you like to do?')
    if command == '' or command == '/dis':
        continue
    if command == '/help':
        print("/create_room $ROOMNAME: Create a new room\n/list_rooms: List all existing rooms\n/join_room $ROOMNAME: Join a specified room\n/select_room $ROOMNAME: Set which room to send messages to\n/leave_room $ROOMNAME: Leave a specified room\n/list_members $ROOMNAME: List the members of a specified room\n/priv_msg $USERNAME $MESSAGE: Send a private message to a specified user\n/dis: Disconnect from the server")
    elif command[0] == '/':
        if command.startswith('/select_room'):
            CURR_ROOM = command.split(' ')[1]
            print(f"Messages will now be sent to {CURR_ROOM}")
        else:
            client.send(command.encode())
    else:
        # User is sending message to current room
        
        client.send(json.dumps({ 'user': user, 'room': CURR_ROOM, 'message': command}).encode())
client.send(command.encode())
print('Quitting...')
client.close()
