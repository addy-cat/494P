#!/usr/bin/env python3
import socket

client = socket.socket()
client_message = input("Your message: ")

client.connect(("0.0.0.0",8080))

client.send(bytearray(client_message, encoding='utf8'))
print(client.recv(8192).decode())


