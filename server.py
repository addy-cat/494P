#!/usr/bin/env python3
import socket
import threading
from server_functions import *

IP = '0.0.0.0'
PORT = 8080

#Dictionary of commands
commands = {
    "/create_room": create_room,
    "/list_rooms": list_rooms,
    "/join_room": join_room,
    "/leave_room": leave_room,
    "/list_members": list_members,
    "/priv_msg": priv_msg,
    "/dis": disconnect
}

def foreach_user(sock, connection):
    # Get username from user
    user = connection.recv(8192).decode().strip()
    Users[user] = connection
    print(f'{user} has connected to the server')
    while True:
        reply = connection.recv(8192).decode()
        if reply == '':
            continue
        if reply[0] == '/':
            command_list = reply.split(' ')
            if len(command_list) == 3:
                command, arg, message = command_list
            elif len(command_list) == 2:
                command, arg, message = command_list + [None]
            elif len(command_list) == 1:
                command, arg, message = command_list + [None, None]
            else:
                command, arg = command_list[0:2]
                message = ' '.join(command_list[2:]) 
            if command in commands:
                commands[command](user, arg, message, connection)
            else:
                print(f"Command {command} does not exist!")
                connection.send(b"Server received a command it didn't understand")
        else:
            request = json.loads(reply)   
            # Send message
            # - Maybe create function to handle this in server_functions.py?
            # request = { user: "username", room: "roomname", message: "message" }
            # send "message" to everyone in room "roomname" and also say that it was from "username"
            send_message_to_room(request['user'], request['room'], request['message'])

#Create socket for server, with port 8080 and interface 0.0.0.0 to listen on
socket = socket.create_server((IP, PORT))
print(f'Server listening on {IP}:{PORT}')

while(True):
    #Listen for connections to the server
    socket.listen(5)
    #Store variable that represents the connection between client and server
    connection = socket.accept()[0]
    print("A client has connected")
    new_thread = threading.Thread(
        group=None,
        target=foreach_user,
        name=None,
        args=(socket, connection),
        kwargs={}
    )
    new_thread.start()
