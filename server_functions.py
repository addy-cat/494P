import socket
import json

#create_room, list_rooms, select_room, join_room, leave_room
class Room():
    def __init__(self):
        # user = (username, connection)
        self.Users = []
        
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
    RoomList[roomname].Users.append((user,connection))
    print(f"{user} joined room {roomname}")
    connection.send(f"You joined room {roomname}".encode())

def leave_room(user, roomname, message, connection):
    len_users = len(RoomList[roomname].Users)
    for i in RoomList[roomname].Users:
        print(i[0])
        if i[0] == user:
            RoomList[roomname].Users.remove(i)
    if len_users > len(RoomList[roomname].Users):
        print(f"{user} left room {roomname}")
        connection.send(f"You left room {roomname}".encode())
    else:
        print(f"{user} tried to leave room they werent in")
        connection.send(f"You are not in room {roomname}".encode())

def list_members(user, roomname, message, connection):
    connection.send(json.dumps([ x[0] for x in RoomList[roomname].Users ]).encode())
    print(f"{user} requested to list members of room {roomname}")

def priv_msg(user, user_to_message, message, connection):
    Users[user_to_message].send(f'(PRIV){user}: {message}'.encode())
def disconnect(user, arg, message, connection):
    print(f"{user} disconnected")
    for i in RoomList:
        if user in i.Users:
            i.Users.pop(user)
    # Maybe tell user that the server is closing their connection?
    connection.close()
    exit()

def send_message_to_room(user, room, message):
    for u in RoomList[room].Users:
        u[1].send(f"\n{user}: {message}".encode())
    print(f"{user} sent message to user in room {room}")
