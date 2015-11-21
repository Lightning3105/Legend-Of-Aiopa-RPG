import gameScreens
import setupScripts
import cProfile
import pstats
if __name__ == "__main__":
    #cProfile.run("gameScreens.mainMenu()", "Out.txt")
    #p = pstats.Stats("Out.txt")
    #p.strip_dirs().sort_stats("time").print_stats(20)
    gameScreens.story()
    
    #gameScreens.game()