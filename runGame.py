#!/usr/bin/env python3

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
    print("START GAME")
    cProfile.run("gameScreens.mainMenu()", "Out.txt")
    with open("Calltime Dump.txt", "w") as fc:
        p = pstats.Stats("Out.txt", stream=fc)
        p.strip_dirs().sort_stats("time").print_stats()
    #gameScreens.story()
    
    #gameScreens.game()
