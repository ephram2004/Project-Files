import string
import random
import time
import numpy as np
import re


class Categories:
    def __init__(self, categories, answer=""):
        self.categories = categories
        self.answer = answer

    def __str__(self):
        return f"{self.categories}"

    @property
    def answer(self):
        return self._answer

    @answer.setter
    def answer(self, newAnswer):
        self._answer = newAnswer


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


def GetCategories():
    """
    Opens the categories.txt files and randomly selects 10 categories to find words for.
    Outputs the 10 numbered categories.

    Parameters
    ------------------
    none

    Returns
    ------------------
    Categories
            object containing the randomly selected categories
    """

    categoriesFile = open('categories.txt', 'r')        #opens categories txt file
    categories = categoriesFile.readlines()             #maps every line to list
    selectedCategories = np.random.choice(range(106), 10, replace=False)    #creates array with 10 random numbers (0-106)
    curCat = 0
    selectList = []
    for i in selectedCategories:                        #loop to output the random categories for this run
        curCat+=1
        print(f'{curCat:>2}. {categories[i]}')
        selectList.append(categories[i][:-1])           #sets categories into list

    results = Categories(selectList)                    #creates Categories object with items from list
    return results                                      #returns created object


def StartGame():
    """
    Starts the game, outputs 10 random categories by calling GetCategories().
    Counts down from 120 seconds and asks the user to continuously input words 
    that match with the given categories.

    Parameters
    ------------------
    none

    Returns
    ------------------
    none
    """

    print("Starting Game\n")    
    usrWords = ""                                   
    startTime = time.time()                         #gets current time
    results = GetCategories()                       #calls functions to print random categories, gets object
    while time.time() - startTime <= 10:            #120 second timer
        usrWords += str(input())                    #continuously get user input

    results._answer = usrWords

    print(results)
    


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
        match usrOption:                                    #calls function depending on user input
            case 1:
                StartGame()                                 #starts game if input is 1
                break
            case 2:     
                continue                                    #loops again to randomize letter
            case 3:
                break                                       #breaks out of while loop to end program
            case _:
                print("Invalid Option. Please Try Again.")  #in case user input is invalid


MainMenu()