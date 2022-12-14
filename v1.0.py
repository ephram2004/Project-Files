import string
import random
import time
import numpy as np
import re


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
        self.orderedAnswers = dict.fromkeys(range(10))

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

        answerPattern = re.compile(r'([1-9])\s?([A-Za-z\'\- ]{1,25})')
        answerMatch = answerPattern.finditer(self._answer)
        for match in answerMatch:
            self.listOfAnswers.append(match[0])

    def AnswerToDict(self):
        """
        Handles the list of answers and assigns them to corresponding keys in dictionary.
        Removes spaces and fills in empty dictionary values for output.
        """

        for currAns in self.listOfAnswers:
            currIndex = int(currAns[0])
            newAns = currAns[1:]
            if newAns[0] == " ":
                newAns = newAns[1:]
            self.orderedAnswers[currIndex] = newAns
            for i in range(10):
                if not self.orderedAnswers[i]:
                    self.orderedAnswers[i] = "\u2717"

    def PrintOutput(self):
        """
        Prints the categories and their corresponding answers to finish the game.
        """

        for i in range(9):
            print(f"{i+1}.  {self.categories[i]:<32}\t{self.orderedAnswers[i+1]}")
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


def GetCategories():
    """
    Opens the categories.txt files and randomly selects 9 categories to find words for.
    Outputs the 9 numbered categories.

    Returns
    ------------------
    Categories
            object containing the randomly selected categories
    """

    categoriesFile = open('categories.txt', 'r')        #opens categories txt file
    categories = categoriesFile.readlines()             #maps every line to list
    selectedCategories = np.random.choice(range(106), 9, replace=False)    #creates array with 10 random numbers (0-106)
    curCat = 0
    selectList = []
    for i in selectedCategories:                        #loop to output the random categories for this run
        curCat+=1
        print(f'{curCat}. {categories[i]}')
        selectList.append(categories[i][:-1])           #sets categories into list

    results = Categories(selectList)                    #creates Categories object with items from list
    return results                                      #returns created object


def StartGame():
    """
    Starts the game, outputs 9 random categories by calling GetCategories().
    Counts down from 100 seconds and asks the user to continuously input words 
    that match with the given categories. Uses object-oriented programming to handle
    user input and return proper data.
    """

    print("100 Seconds Start NOW!\n")    
    usrWords = ""                                   
    startTime = time.time()                         #gets current time
    results = GetCategories()                       #calls functions to print random categories, gets object
    while time.time() - startTime <= 100:           #100 second timer
        usrWords += str(input())                    #continuously get user input

    print("\n")
    results._answer = usrWords

    results.GetAnswers()
    results.AnswerToDict()
    results.PrintOutput()


def MainMenu():
    """
    Directs the program to the proper functions based on user-requested inputs. Outputs
    random letter and asks user to roll again or begin the game.
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