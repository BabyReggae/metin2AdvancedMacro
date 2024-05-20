# main.py

# Importing the class from the game module
from classes.game import Game

def main():
    # Creating an instance of the Game class
    game_instance = Game()

    # Now you can use methods and attributes of the game_instance
    game_instance.start()

if __name__ == "__main__":
    main()
