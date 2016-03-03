import pygame as py
from Multiplayer import MPvariables as v
import requests
import json
import pickle
import threading
import time
from ast import literal_eval

py.init()
v.screen = py.display.set_mode((300, 300))


def start():
    t1 = threading.Thread(target=server)
    t1.start()
    game()
    
def server():
    while True:
        t = time.clock()
        payload = {"username": v.username, "position": (v.posx, v.posy)}
        jpayload = json.dumps(str(payload))
        r = requests.post(v.url, data=jpayload)
        # Response, status etc
        if r.status_code == 200:
            v.data = literal_eval(r.text)
            v.fetched = True
            v.pastdata = {}
        else:
                print(r.status_code)
                print(r.text)
        v.fetchTime = time.clock() - t
        #fetchTime = 8
        #print(fetchTime)

def game():
    v.clock = py.time.Clock()
    while True:
        py.event.pump()
        v.clock.tick(30)
        #print(clock.get_fps())
        v.screen.fill((0, 0, 0))
        py.draw.rect(v.screen, (0, 0, 255), (v.posx, v.posy, 50, 50))
        #posx, posy = py.mouse.get_pos()
        pressed = py.key.get_pressed()
        if pressed[py.K_a]:
            v.posx -= 5
        if pressed[py.K_d]:
            v.posx += 5
        if pressed[py.K_w]:
            v.posy -= 5
        if pressed[py.K_s]:
            v.posy += 5
        for name, values in v.data["players"].items():
            if not name == v.username:
                if values["online"]:
                    if v.fetched == False:
                        if name in v.vectors.keys():
                            values["position"] = (values["position"][0] + v.vectors[name][0], values["position"][1] + v.vectors[name][1])
                    else:
                        if not values["position"] == None:
                            if name in v.pastdata.keys():
                                v.vectors[name] = ((values["position"][0] - v.pastdata[name][0]) / (30 * v.fetchTime), (values["position"][1] - v.pastdata[name][1]) / (30 * v.fetchTime))
                                print(v.vectors[name])
                            v.pastdata[name] = values["position"]
                    #print(values["position"])
                    py.draw.rect(v.screen, (255, 0, 0), (values["position"], (50, 50)))
                    if not name in v.pastdata.keys():
                        v.pastdata[name] = []
                    v.fetched = False
        
        py.display.flip()