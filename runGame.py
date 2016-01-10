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
    cProfile.run("gameScreens.mainMenu()", "Out.txt")
    p = pstats.Stats("Out.txt")
    p.strip_dirs().sort_stats("time").print_stats(20)
    #gameScreens.story()
    
    #gameScreens.game()
