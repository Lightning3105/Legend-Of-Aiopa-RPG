import pygame as py
from Multiplayer import MPvariables as v
import Variables as va
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
    t1 = threading.Thread(target=serverLoop)
    t1.start()
    va.debug("Start Game")
    game()
    va.debug("After game")
    payload = {"username": v.username, "disconnect": True}
    jpayload = json.dumps(str(payload))
    r = requests.post(v.url, data=jpayload)
    v.stopped = True
    
def serverLoop():
    while True:
        server()
        if v.stopped:
            return
        
def server():        
    t = time.clock()
    payload = {"username": v.username, "position": (v.posx, v.posy)}
    jpayload = json.dumps(str(payload))
    try:
        r = requests.post(v.url, data=jpayload)
    except Exception as e:
        va.debug(e)
    # Response, status etc
    if r.status_code == 200:
        v.data = literal_eval(r.text)
        v.fetched = True
    else:
        print(r.status_code)
        print(r.text)
    #print(v.data)
    v.fetchTime = time.clock() - t
    #fetchTime = 8
    #print(fetchTime)

def game():
    v.clock = py.time.Clock()
    ping = MenuItems.textLabel("Ping: 0", (320, 10), (255, 0, 0), "Resources/Fonts/RPGSystem.ttf", 20, centred=True, screen=v.screen)
    server()
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
        ping.text = "Ping: " + str(round(v.fetchTime * 1000, 1))
        for event in py.event.get():
            if event.type == py.KEYDOWN:
                if event.key == py.K_ESCAPE:
                    return
        for name, values in v.data["players"].items():
            if not "position" in values:
                values["position"] = (0, 0)
            if not name == v.username:
                if values["online"]:
                    if v.fetched == False:
                        if name in v.vectors.keys():
                            values["position"] = (values["position"][0] + v.vectors[name][0], values["position"][1] + v.vectors[name][1])
                    else:
                        print("VALUES POS", values)
                        if not values["position"] == None:
                            if name in v.pastdata.keys():
                                v.vectors[name] = ((values["position"][0] - v.pastdata[name][0]) / (30 * v.fetchTime), (values["position"][1] - v.pastdata[name][1]) / (30 * v.fetchTime))
                            v.pastdata[name] = values["position"]
                    #print(values["position"])
                    py.draw.rect(v.screen, (255, 0, 0), (values["position"], (50, 50)))
                    MenuItems.textLabel(name, (values["position"][0] + 25, values["position"][1] - 40), (255, 255, 255), "Resources/Fonts/RPGSystem.ttf", 20, centred=True, screen=v.screen).update()
                    if not name in v.pastdata.keys():
                        v.pastdata[name] = []
                    v.fetched = False
        ping.update()
        py.display.flip()
