#!/usr/bin/env python3
import gameScreens
#import setupScripts
import cProfile
import pstats
#import pickle
import SaveLoad
import pygame as py
import traceback
import time
import os
from importlib import reload

def main(func="mainMenu"):
    print("START GAME")
    try:
        cProfile.run("gameScreens." + func + "()", "Out.txt")
    except Exception as e:
        if "Reload:" in str(e):
            curFunc = str(e).strip("Reload:")
            print("Reload:", curFunc)
            reload(gameScreens)
            main(curFunc)
        print("EXCEPTION:")
        print(traceback.print_exc())
        if not os.path.exists("Crash Reports"):
            os.makedirs("Crash Reports")
        name = "Crash Reports/Crash Report " + time.strftime("%Y-%m-%d_%H.%M.%S") + ".txt"
        with open(name, "w") as crash:
            a = traceback.print_exc(file=crash, limit=8)
        with open(name, "r") as crash:
            gameScreens.crashScreen(crash.read())
    py.quit()
    with open("Calltime Dump.txt", "w") as fc:
        p = pstats.Stats("Out.txt", stream=fc)
        p.strip_dirs()
        d = p.__dict__["stats"]
        funcstats = {}
        
        for k, v in d.items():
            funcstats[k] = v[2]
        p.sort_stats("time").print_stats()
        SaveLoad.uploadStats(funcstats)

    with open("Calltime Dump.txt", "rb") as fc:
        pass

if __name__ == "__main__":
    main()