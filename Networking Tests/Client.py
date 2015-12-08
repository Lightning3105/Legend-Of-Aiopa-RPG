# client.py  
import socket
import pickle

# create a socket object
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

# get local machine name
host = socket.gethostname()                           

port = 9999

# connection to hostname on the port.
s.connect((host, port))                               

# Receive no more than 1024 bytes
ID = s.recv(1024)                                     

print("The client ID is %s" % ID.decode('ascii'))

import pygame as py
screen = py.display.set_mode((200, 200))

positions = {}

while True:
    py.event.pump()
    screen.fill((0, 0, 0))
    pos = (py.mouse.get_pos()[0] - 10, py.mouse.get_pos()[1] - 10)
    size = (20, 20)
    py.draw.rect(screen, (255, 0, 0), (pos, size))
    s.send(pickle.dumps(pos))
    positions = pickle.loads(s.recv(1024))
    for key, value in positions.items():
        if int(key) != int(ID):
            py.draw.rect(screen, (0, 0, 255), (value, (20, 20)))
    py.display.flip()
    