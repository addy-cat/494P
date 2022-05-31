#!/usr/bin/env python3
import socket
import threading

#Dictionary of commands
commands = {
    "/create_room": create_room,
    "/list_rooms": list_rooms,
    "/select_room": select_room,
    "/join_room": join_room,
    "/leave_room": leave_room,
    "/list_members": list_members,
    "/priv_msg": priv_msg,
    "/dis": disconnect
}


#Create socket for server, with port 8080 and interface 0.0.0.0 to listen on
socket = socket.create_server(("0.0.0.0", 8080))

while(True):
    #Listen for connections to the server
    socket.listen(5)
    #Store variable that represents the connection between client and server
    connection = socket.accept()[0]
    print("A client has connected")
    new_thread = threading.Thread(
        None,
        foreach_user,
        None,
        (connection)
    )
    new_thread.start()

def foreach_user(connection):
    # Get username from user
    user = connection.recv(8192).decode()
    while True:
        reply = connection.recv(8192).decode()
        if reply[0] == '/':
            command, arg, message = reply.split(' ')
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

def
