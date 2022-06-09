import socket
import json

#create_room, list_rooms, select_room, join_room, leave_room
class Room():
    def __init__(self):
        # Users = { user1: connection1, user2: connection2 }
        # Assignment: Users[user1] = connection1
        # Access: connect = Users[user1] //Stores connection1 in connect
        # list of users in a room
        self.Users = {}
        
RoomList = {}
Users = {}
# Each function needs to do three things:
# - Action
# - log action to server output (e.g. print("ACTION OCCURRED"))
# - notify user that action occurred (e.g. connection.send("YOU DID THE ACTION"))

def create_room(user, roomname, message, connection):
    RoomList[roomname] = Room()
    print(f"{user} created room {roomname}")
    connection.send(f"Room {roomname} created".encode())

def list_rooms(user, arg, message, connection):
    connection.send(json.dumps(list(RoomList.keys())).encode())
    print(f"{user} requested list of rooms")

def join_room(user, roomname, message, connection):
    RoomList[roomname].Users[user] = connection
    print(f"{user} joined room {roomname}")
    connection.send(f"You joined room {roomname}".encode())

def leave_room(user, roomname, message, connection):
    #get the length of the roomlist
    len_users = len(RoomList[roomname].Users)
    #if the user is in the list of users that are in the room delete them from users list
    if user in RoomList[roomname].Users:
        del RoomList[roomname].Users[user]
    if len_users > len(RoomList[roomname].Users):
        print(f"{user} left room {roomname}")
        connection.send(f"You left room {roomname}".encode())
    else:
        print(f"{user} tried to leave room they werent in")
        connection.send(f"You are not in room {roomname}".encode())

def list_members(user, roomname, message, connection):
    #dump the json data for the list of users in a room and sends it to the client
    connection.send(json.dumps(list(RoomList[roomname].Users.keys())).encode())
    print(f"{user} requested to list members of room {roomname}")

def priv_msg(user, user_to_message, message, connection):
    Users[user_to_message].send(f'(PRIV) {user}: {message}'.encode())
def disconnect(user, arg, message, connection):
    print(f"{user} disconnected")
    #go through each room, if the user was in that room then delete them
    for i in RoomList.values():
        if user in i.Users:
            del i.Users[user]
    # Maybe tell user that the server is closing their connection?
    connection.close()
    exit()

def send_message_to_room(user, room, message):
    #u is a users connection
    for u in RoomList[room].Users.values():
        u.send(f"\n{user}: {message}".encode())
    print(f"{user} sent message to users in room {room}")
