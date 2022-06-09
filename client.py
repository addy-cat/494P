#!/usr/bin/env python3
import socket
import json
import threading
import sys

IP = '0.0.0.0'
PORT = 8080
CURR_ROOM = ''
def prompt(user):
    return input(f'{user}> ')    #input is how you get user input from command line
# Usage: print(prompt('redawl'))

def message_handler(sock, placeholder):
    prev_len = 0
    while True:
        try:
            message = sock.recv(8192).decode()
            #if message is zero then maybe the server crashed. so just stop handling messages.
            if len(message) == 0:
                return
            print(" " * prev_len, end='')
            print('\r' + message + f'\n{user}> ', end='')
        except:
            return
        prev_len = len(message)

#the socket for the client to connect to the server
client = socket.socket()

client.connect((IP,PORT))
print(f'Connecting to {IP}:{PORT}')

user = input('Enter your username > ')
client.send(user.encode())
print("Welcome to server! type '/help' for info")
# Set up listener for room messages, if another user sends us a message
new_thread = threading.Thread(
    group=None,
    target=message_handler, # Name of the function that new_thread calls
    name=None,
    args=(client, None), # arguments to the function that new_thread calls
    kwargs={}
)  
new_thread.start()
command = ''
while command != '/dis':
    #when there is one thread its just us
    if threading.active_count() == 1:
        print('Server closed, exiting...')
        exit()
    command = prompt(user)
    if command == '' or command == '/dis':
        continue
    if command == '/help':
        print("/create_room $ROOMNAME: Create a new room\n/list_rooms: List all existing rooms\n/join_room $ROOMNAME: Join a specified room\n/select_room $ROOMNAME: Set which room to send messages to\n/leave_room $ROOMNAME: Leave a specified room\n/list_members $ROOMNAME: List the members of a specified room\n/priv_msg $USERNAME $MESSAGE: Send a private message to a specified user\n/dis: Disconnect from the server")
    elif command[0] == '/':
        #if the user ran the select room command, the current room to start sending messages to is in CURR ROOM
        if command.startswith('/select_room'):
            CURR_ROOM = command.split(' ')[1]
            print(f"Messages will now be sent to {CURR_ROOM}")
            
        else:
            #if list members is used then split the command into the list_members command and the roomname to list members of
            #if the user just said list_rooms
            if command.startswith('/list_members') and len(command.split(' ')) < 2:
                print("You must specify a room to list users")
            else:
                #encode all others commands and send to server 
                client.send(command.encode())
    #else we just want to send a message to the current room
    else:
        # User is sending message to current room
        if CURR_ROOM == '':
            print('You must select a room with /select_room first')
        else:
            #send the server the username, current room theyre in and the command they ran
            client.send(json.dumps({ 'user': user, 'room': CURR_ROOM, 'message': command}).encode())

client.send(command.encode())
print('Quitting...')
client.close()
