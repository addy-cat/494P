#!/usr/bin/env python3
import socket
import threading
from server_functions import *

#IP address listening on
IP = '0.0.0.0'
#Port on IP address listening on
PORT = 8080

#Dictionary of commands to functions, can be called by foreach_user
commands = {
    "/create_room": create_room,
    "/list_rooms": list_rooms,
    "/join_room": join_room,
    "/leave_room": leave_room,
    "/list_members": list_members,
    "/priv_msg": priv_msg,
    #disconnect from server
    "/dis": disconnect
}

#Runs for each user 
def foreach_user(sock, connection):    #connection is the connection between the server and the client
    # Get username from user, recv for recieving username from client, decode to make a string instead of bytes
    user = connection.recv(8192).decode().strip()   #user is whatever is recieved from the client, in this case the username
    Users[user] = connection                        #Users is an array of users, where the index is a user, store the connection in that index, so whenever we need to talk to a user we just pass their username to the Users list
    print(f'{user} has connected to the server')
    while True:
        reply = connection.recv(8192).decode()    #reply is the data recieved from the user, decode from raw bytes to string
        if reply == '':
            continue
        if reply[0] == '/':
            command_list = reply.split(' ')       #splits the command from the args from user
            if len(command_list) == 3:            #if there are three parts to the command, arg part, message such as priv_msg command
                command, arg, message = command_list
            elif len(command_list) == 2:          #if there are two commands, command_list gets command for 1st arg, arg for 2nd arg, None for 3rd
                command, arg, message = command_list + [None]
            elif len(command_list) == 1:
                command, arg, message = command_list + [None, None]
            else:   
                #If more than three substrings in the command, command is 1st arg, arg is 2nd arg,
                command, arg = command_list[0:2]
                #allows for messages with spaces for the message part of a command, such as a priv_msg, for 3rd arg
                message = ' '.join(command_list[2:]) 
            #if the parsed for command is in the commands dictionary, then: 
            if command in commands:
                #then call the function that cooresponded to that command with these arguments
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

#Used to kick users
def control(sock, dummy):
    command = ''
    while command != '/quit':
        command = input('Server > ')
        #kicks a user by username
        if command.startswith('/kick'):
            user = command.split(' ')[1]
            Users[user].send('You got kicked....'.encode())
            #closes users connection
            Users[user].close()
            #pops them off the user list
            Users.pop(user)

#Create socket for server, with port 8080 and interface 0.0.0.0 to listen on
socket = socket.create_server((IP, PORT))
print(f'Server listening on {IP}:{PORT}')

#control_thread is for the person who is controlling the server, whoever types "./server.py"
#used to kick users. threading.Thread is defining the thread for the server operator.
control_thread = threading.Thread(
    group=None,
    target=control, # name of function that the thread "control_thread" calls
    name=None,
    args=(socket, None), # arguments, for some reason if there is just one argument here for args, threading.Thread crashes
    kwargs={}
)
#start the new thread
control_thread.start()

while(True):
    #Listen for connections to the server
    socket.listen(5)
    #Store variable that represents the connection between client and server
    #connection is used to communicate to the client that connected, and is used to recieve data from the cliient
    connection = socket.accept()[0]
    print("A client has connected")
    #Thread (seperate instance of the program for each user)
    new_thread = threading.Thread(
        group=None,
        #
        target=foreach_user, #Function that the thread new_thread calls
        name=None,
        args=(socket, connection), #Function args
        kwargs={}
    )
    new_thread.start()
    
