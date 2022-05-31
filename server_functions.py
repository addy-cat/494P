import socket

#create_room, list_rooms, select_room, join_room, leave_room
class Room():
    def __init__(self):
        # user = (username, connection)
        self.Users = []
        
RoomList = {}
# Each function needs to do three things:
# - Action
# - log action to server output (e.g. print("ACTION OCCURRED"))
# - notify user that action occurred (e.g. connection.send("YOU DID THE ACTION"))

def create_room(user, roomname, message, connection):
    RoomList[roomname] = Room()
def list_rooms(user, arg, message, connection):
    connection.send(json.dumps(Rooms.keys()))
    print(f"{user} requested list of rooms")
def select_room(user, arg, message, connection):

def join_room(user, roomname, message, connection):
    RoomList[roomname].Users.append(user)
    
def leave_room(user, roomname, message, connection):

def list_members(user, roomname, message, connection):

def priv_msg(user, user_to_message, message, connection):

def disconnect(user, arg, message, connection):
    print(f"{user} disconnected")
    # Maybe tell user that the server is closing their connection?
    connection.close()
