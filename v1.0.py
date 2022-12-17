#ScatterFolie - Created by Ephram Cola Jacquin

import string
import random
import time
import numpy as np
import re
from threading import Thread
import os
from tkinter import *
import sys

usrWords = ""                   #initializing variables
countLimit = 100
nmbrCat = 10

class Categories:
    """
    A class to represent a game of categories.

    Attributes
    ------------------
    categories : list-of-strings
        list of randomly selected categories
    answer : str
        raw string of user answers
    listOfAnswers : list-of-string
        list of individual user answers ordered by category number
    orderedAnswers : dictionary[int: "string"]
        pairs final answers to categories

    Methods
    ------------------
    GetAnswers():
        Uses RegEx to separate individual answers.
    AnswerToDict():
        Orders answers into dictionary
    PrintOutput():
        Prints the categories and corresponding answers in order
    """

    def __init__(self, categories, answer="", listOfAnswers=[]):
        """
        Constructs attributes for the object.

        Parameters
        ------------------
        categories : list-of-strings
            list of randomly selected categories
        answer : str
            raw string of user answers
        listOfAnswers : list-of-string
            list of individual user answers ordered by category number
        orderedAnswers : dictionary[int: "string"]
            pairs final answers to categories

        """
        self.categories = categories
        self.answer = answer
        self.listOfAnswers = listOfAnswers
        self.orderedAnswers = dict.fromkeys(range(nmbrCat+1))

    def __str__(self):
        """
        (Debugging) Prints created dictionary.

        Returns
        ------------------
        dict
            dictionary of categories and answers
        """
        return f"{self.orderedAnswers}"

    @property
    def answer(self):
        """
        Outputs value of raw answer string.

        Returns
        ------------------
        str
            raw string of user-inputted answers
        """
        return self._answer

    @answer.setter
    def answer(self, newAnswer):
        """
        Sets the raw answer string.

        Parameters
        ------------------
        newAnswer : str
                   user-given answers
        """
        self._answer = newAnswer

    def GetAnswers(self):
        """
        Splits raw string into individually numbered answers using Regular Expressions.
        Checks for digit followed by space followed by characters or special characters.
        Outputs the answers into a list
        """

        answerPattern = re.compile(r'([1-9])[0-9]?\s?([A-Za-z\'\-\& ]{1,50})')  #splits answers from raw string
        answerMatch = answerPattern.finditer(self._answer)                      #finds answers using instructions above
        for match in answerMatch:                                               #maps all answers to a list 
            self.listOfAnswers.append(match[0])

    def AnswerToDict(self):
        """
        Handles the list of answers and assigns them to corresponding keys in dictionary.
        Removes spaces and fills in empty dictionary values for output.
        """

        for currAns in self.listOfAnswers:                  #handles each answer in list
            if nmbrCat > 9:                                 #if two digit category number
                currIndex = int(currAns[0:2])               #changes the first two digits to int type
                newAns = currAns[2:].title()                #removes number from answer
            else:                                           #if one digit category number
                currIndex = int(currAns[0])                 #changes the first digit to int type
                newAns = currAns[1:].title()                #removes digit from answer
            if newAns[0] == " ":                            #if extra whitespace is at start of answer, remove it
                newAns = newAns[1:].title()                 #every word is uppercase
            self.orderedAnswers[currIndex] = newAns         #add answer to corresponding key in dict
            for i in range(nmbrCat + 1):                    #replace empty dict values with a cross
                if not self.orderedAnswers[i]:
                    self.orderedAnswers[i] = "\u2717"

    def PrintOutput(self):
        """
        Prints the categories and their corresponding answers to finish the game.
        """

        for i in range(nmbrCat):                            #prints category number, category, and corresponding answer
            if i < 9:                                       #for consistent spacing (depending on number of digits)
                print(f"{(i+1):}.   {self.categories[i]:<32}\t{self.orderedAnswers[i+1]}")
            else:
                print(f"{(i+1):}.  {self.categories[i]:<32}\t{self.orderedAnswers[i+1]}")
        print("\n")


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

def ChngTimer():
    """
    Changes the countdown value by asking the user for a new value.
    The default value is set to 100 seconds.
    """
    global countLimit                                                               #set countLimit scope to global
    countLimit = int(input("Enter counter value in seconds (max: 999):\n"))         #ask user to enter counter limit

def ChngCat():
    """
    Changes the number of randomly generated categories.
    The default value is set to 10.
    """

    global nmbrCat                                                                  #set nmbrCat scope to global
    nmbrCat = int(input("Enter number of random categories to generate (1-99)\n"))  #ask user to enter number


def GetCategories():
    """
    Opens the categories.txt files and randomly selects 9 categories to find words for.
    Outputs the 9 numbered categories.

    Returns
    ------------------
    Categories
            object containing the randomly selected categories
    """

    categoriesFile = open('categories.txt', 'r')                                #opens categories txt file
    categories = categoriesFile.readlines()                                     #maps every line to list
    selectedCategories = np.random.choice(range(106), nmbrCat, replace=False)   #creates array with n random numbers (0-105)
    curCat = 0
    selectList = []
    for i in selectedCategories:                        #loop to output the random categories for this run
        curCat+=1
        print(f'{curCat}. {categories[i]}')
        selectList.append(categories[i][:-1])           #sets categories into list

    results = Categories(selectList)                    #creates Categories object with items from list
    return results                                      #returns created object


def GetInput():
    """
    Fetches the continuous user input stream from the console. Contains an infinite loop so that the user
    can keep entering data. This function is stopped as soon as the counter runs out. Variables are called
    globally because return statements in Thread functions are diffiult to manage.
    """
    
    global usrWords                                     #globally declare variable
    while True:                                         #continously fetch input user text as a large appended string
        usrWords += sys.stdin.readline()


def Counter():
    """
    Keeps track of elapsed time and handles the user answer data to output the answers once the game is finished.
    Exits the program after outputting the data, closing all functions and stopping the console from fetching
    input data.
    """

    global startTime                                    #globally declare variable
    startTime = time.time()                             #get the time of game start
    results = GetCategories()                           #calls functions to print random categories, gets object
    while True:
        if time.time() - startTime == countLimit:       #when the counter reaches the limit
            print("\nTime is up!")                      #announce game end
            print("\n")

            results._answer = usrWords                  #create object with answers constructor
            results.GetAnswers()                        #call function to handle raw string
            results.AnswerToDict()                      #call function to move answer list to dict
            results.PrintOutput()                       #call function to print the results

            os._exit(1)                                 #exits the entire program


def StartGame():
    """
    Starts the game, uses threading to call the Counter() and GetInuput() functions simultaneously
    This method stops the input from fetching console data as soon as the counter expires. Includes 
    Tkinter library to display timer as it is counting down.
    """                                

    answer = Thread(target=GetInput)                    #assign GetInput thread
    counter = Thread(target=Counter)                    #assign Counter thread
    answer.start()                                      #run GetInput function
    counter.start()                                     #run Counter function simultaneously

    win = Tk()                                          #initialize Tk window
    win.geometry('300x300')                             #set display size
    win.resizable(False, False)                         #non-scalable
    win.config(bg='#EBECF0')                            #background color
    timeLeft = StringVar()                              #initialize variable as "image string"
    Entry(win, textvariable=timeLeft, width=3, font='Helvetica 48').place(x=110, y=110)     #text style
    while True:
        currTime = countLimit - (time.time() - startTime) + 1   #countdown from set limit
        timeLeft.set(f'{str(int(currTime))}')                   #output seconds converted from float to integer
        win.update()                                            #update the GUI

def MainMenu():
    """
    Directs the program to the proper functions based on user-requested inputs. Outputs
    random letter and asks user to roll again or begin the game.
    """

    print("\nWelcome to ScatterFolie!")

    letterToPlay = 'A'                                      #initialize variables
    usrOption = 0

    while usrOption != 6:                                   #asks for user option input
        if usrOption == 3 or usrOption == 0:                #randomize letter when needed
            letterToPlay = RandLetter(letterToPlay)         #calls function to output random letter
        print(f'\nCurrent Letter is: {letterToPlay}')       #prints letter to play with
        print(f'Timer is set to {countLimit} seconds')      #prints timer limit
        print(f'Number of categories is: {nmbrCat}\n')      #prints number of generated categories
        usrOption = int(input(f"Select an option:\n1. Open instructions\n2. Start game\n3. Re-Roll letter\n\
4. Change time limit (default is 100s)\n5. Change number of categories (default is 10)\n6. Exit\n"))
        match usrOption:                                    #calls function depending on user input
            case 1:
                print("\nWhen selecting \"start game\" the console will output a set of 9 randomly \
generated categories.\nThe player must find a word starting with the given letter that matches with \
each category.\nTo give an answer, enter the category's number, followed by a space, followed \
by the word or\nexpression. Press enter to submit the answer. An example of a valid answer is: \
\"4 Northeastern.\"\nSpecial characters, such as -, &, and ', are also accepted, as long as they are \
preceeded by a word.\nAnswers do not have to be given in order. If you find a new word for an already \
answered category,\nsimply write the new answer with the corresponding category number, and the program \
will automatically\nreplace an old answer with the most recent one. Good luck!")
            case 2:
                print("\n")
                StartGame()                                 #starts game if input is 1
            case 3:     
                continue                                    #loops again to randomize letter
            case 4:
                ChngTimer()                                 #calls function to change maximum count
            case 5:
                ChngCat()                                   #calls function to change number of categories
            case 6:
                break                                       #breaks out of while loop to end program
            case _:
                print("Invalid Option. Please Try Again.")  #in case user input is invalid


MainMenu()