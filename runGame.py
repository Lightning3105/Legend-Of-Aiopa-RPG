#!/usr/bin/env python3

def tree(d, indent=0):
    for key, value in d.items():
        print ('\t' * indent + str(key))
        if isinstance(value, dict):
            tree(value, indent+1)
        else:
            print ('\t' * (indent+1) + str(value))


if __name__ == "__main__":
    import Updater
    from getpass import getuser
    if not getuser() == "James Waters":
        print(getuser() == "James Waters")
        try:
            Updater.updateCheck()
        except:
            pass
    
    import gameScreens
    import setupScripts
    import cProfile
    import pstats
    import pickle
    
    print("START GAME")
    cProfile.run("gameScreens.mainMenu()", "Out.txt")
    with open("Calltime Dump.txt", "w") as fc:
        p = pstats.Stats("Out.txt", stream=fc)
        p.strip_dirs()
        d = p.__dict__["stats"]
        #print(d)
        
        for k, v in d.items():
            print(k, ":::", v)
        p.sort_stats("time").print_stats()
        
    with open("Calltime Dump.txt", "rb") as fc:
        pass
    #gameScreens.story()
    
    #gameScreens.game()
