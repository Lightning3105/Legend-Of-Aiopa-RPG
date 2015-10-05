import gameScreens
import pstats
import cProfile
if __name__ == "__main__":
    cProfile.run("gameScreens.mainMenu()", "Out.txt")
    
    #gameScreens.game()