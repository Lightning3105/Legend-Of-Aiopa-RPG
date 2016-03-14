import pygame as py
from Multiplayer import MPvariables as v
import requests
import json
import pickle
import threading
import time
from ast import literal_eval
import MenuItems

py.init()
v.screen = py.display.set_mode((300, 300))


def start():
    v.stopped = False
    t1 = threading.Thread(target=server)
    t1.start()
    game()
    print("after game")
    payload = {"username": v.username, "disconnect": True}
    jpayload = json.dumps(str(payload))
    r = requests.post(v.url, data=jpayload)
    v.stopped = True
    
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
        else:
            print(r.status_code)
        #print(r.text)
        #print(v.data)
        v.fetchTime = time.clock() - t
        #fetchTime = 8
        #print(fetchTime)
        if v.stopped:
            return

def game():
    v.clock = py.time.Clock()
    ping = MenuItems.textLabel("Ping: 0", (320, 10), (255, 0, 0), None, 20, centred=True)
    while True:
        print("START")
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
        ping.text = "Ping: " + str(round(v.fetchTime * 1000, 1))
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    print("ESCAPE RETURN")
                    return
        print("PRE ITERATOR")
        for name, values in v.data["players"].items():
            if not name == v.username:
                print("IF NAME")
                if values["online"]:
                    print("IF ONLINE")
                    if v.fetched == False:
                        print("IF FETCHED")
                        if name in v.vectors.keys():
                            print("NAME VECTORS")
                            v.data["players"][name]["position"] = (values["position"][0] + v.vectors[name][0], values["position"][1] + v.vectors[name][1])
                            print("POST NAME VECTORS")
                    else:
                        print("ELSE FETCHED")
                        if not values["position"] == None:
                            print("IF POSITION")
                            if name in v.pastdata.keys():
                                print("NAME PASTDATA")
                                v.vectors[name] = ((values["position"][0] - v.pastdata[name][0]) / (30 * v.fetchTime), (values["position"][1] - v.pastdata[name][1]) / (30 * v.fetchTime))
                            v.pastdata[name] = values["position"]
                    #print(values["position"])
                    py.draw.rect(v.screen, (255, 0, 0), (values["position"], (50, 50)))
                    if not name in v.pastdata.keys():
                        print("NOT NAME PASTDATA")
                        v.pastdata[name] = []
                    v.fetched = False
                    print("DONE", name)
        print("POST ITERATOR")
        ping.update()
        py.display.flip()
        print("END")