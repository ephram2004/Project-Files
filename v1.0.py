import string
import random

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



def StartGame():
    print("Starting Game\n")


def MainMenu():