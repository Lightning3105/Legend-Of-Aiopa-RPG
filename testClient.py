import pygame as py
import json
import requests
from ast import literal_eval
import random
import threading
import time

py.init()
posx = 50
posy = 50
oldposx = 0
oldposy = 0
username = "player " + str(random.randint(0, 999))
#url = "http://socket-lightning3105.rhcloud.com/" + "multiplayer/1"
url = "http://127.0.0.1:5000/" + "multiplayer/1"
screen = py.display.set_mode((300, 300))
data = {"players":{}}
pastdata = {}
vectors = {}
fetched = True
fetchTime = 4



def game():   
    clock = py.time.Clock() 
    global posx
    global posy
    global fetched
    global vectors
    while True:
        py.event.pump()
        clock.tick(30)
        #print(clock.get_fps())
        screen.fill((0, 0, 0))
        py.draw.rect(screen, (0, 0, 255), (posx, posy, 50, 50))
        #posx, posy = py.mouse.get_pos()
        pressed = py.key.get_pressed()
        if pressed[py.K_a]:
            posx -= 5
        if pressed[py.K_d]:
            posx += 5
        if pressed[py.K_w]:
            posy -= 5
        if pressed[py.K_s]:
            posy += 5
        for name, values in data["players"].items():
            if not name == username:
                if values["online"]:
                    if fetched == False:
                        if name in vectors.keys():
                            values["position"] = (values["position"][0] + vectors[name][0], values["position"][1] + vectors[name][1])
                    else:
                        if not values["position"] == None:
                            if name in pastdata.keys():
                                vectors[name] = ((values["position"][0] - pastdata[name][0]) / (30 * fetchTime), (values["position"][1] - pastdata[name][1]) / (30 * fetchTime))
                                print(vectors[name])
                            pastdata[name] = values["position"]
                    #print(values["position"])
                    py.draw.rect(screen, (255, 0, 0), (values["position"], (50, 50)))
                    if not name in pastdata.keys():
                        pastdata[name] = []
                    fetched = False
        
        py.display.flip()

def server():
    global data
    global fetched
    global fetchTime
    while True:
        t = time.clock()
        payload = {"username": username, "position": (posx, posy)}
        jpayload = json.dumps(str(payload))
        r = requests.post(url, data=jpayload)
        # Response, status etc
        if r.status_code == 200:
            data = literal_eval(r.text)
            fetched = True
            pastdata = {}
        else:
                print(r.status_code)
                print(r.text)
        fetchTime = time.clock() - t
        #fetchTime = 8
        #print(fetchTime)

if __name__ == "__main__":
    payload = {"connect": True, "username": username}
    jpayload = json.dumps(str(payload))
    r = requests.post(url, data=jpayload)
    print("START", r.text)
    t1 = threading.Thread(target=server)
    t1.start()
    print("now")
    game()