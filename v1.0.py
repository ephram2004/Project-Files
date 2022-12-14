import string
import random
import time
from threading import Thread

#find a random letter
def RandLetter(currLetter):
    """ 
    Generates a list of all the letters in the alphabet and picks one at random.
        If the randomly generated letter matches with the currently selected letter,
        a new letter is picked.
        
        Parameters
        ------------------
        currLetter : char
                  current selected letter
                  
        Returns
        ------------------
        char
            randomly generated letter
    """

    newLetter = currLetter                              #preset new letter 
    LETTERLIST = list(string.ascii_uppercase)           #set constant alphabet list
    while newLetter is currLetter:                      #to avoid repeating letters
        newLetter = LETTERLIST[random.randrange(26)]
    
    return newLetter                                    #returns the new letter


def Counter():
    """
    Counts down from 120 seconds.

    Parameters
    ------------------
    none

    Returns
    ------------------
    none
    """

    startTime = time.time()
    for i in range(10):
        time.sleep(1)


def StartGame():
    """
    Begins the game. Uses "Thread" to run the timer independently from the user input function.
    Function calls the two separate Counter() and GetInput() functions.
    """

    print("Starting Game\n")
    runTimer = Thread(target=Counter)
    runTimer.start()


def MainMenu():
    """
    Directs the program to the proper functions based on user-requested inputs. Outputs
    random letter and asks user to roll again or begin the game.

    Parameters
    ------------------
    none

    Returns
    ------------------
    none
    """

    letterToPlay = 'A'                                      #initialize variables
    usrOption = 0

    while usrOption != 3:                                   #asks for user option input
        letterToPlay = RandLetter(letterToPlay)             #calls function to output random letter
        print(f'\nCurrent Letter is: {letterToPlay}\n')
        usrOption = int(input(f"Select an option:\n1. Start game\n2. Re-Roll Letter\n3. Exit\n"))
        match usrOption:
            case 1:
                StartGame()
                break
            case 2:
                continue
            case 3:
                break
            case _:
                print("Invalid Option. Please Try Again.")




MainMenu()