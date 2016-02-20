
'''
An Introduction to Interactive Programming in Python - Week 2
Guess the Number
2015-Dec-30
Python 2.7
Chris
'''

import random
import math

'''
# noWins and noLosses counts session win/loss stats.
# secAnswer is the random generated number player must guess at
# countGuess is how many guesses they have made

l/u BoundNo are the limits which the secAnswer is between, tBoundNo is the number of possibilities
noOfGuess is calculated based on formula [log_2 n] + 1 so it is always possible to win using a binary search
'''

secAnswer = 0
countGuess = 0
noWins = 0
noLosses = 0

lBoundNo = 1
uBoundNo = 100
tBoundNo = uBoundNo - lBoundNo + 1
noOfGuess = int(math.log(tBoundNo, 2) + 1)

'''
can add an option to choose higher bound number using raw input

for computer binary search:
 store upper and lower guesses
 work out difference and divide 2 (round!)
 do upper minus dif/2 to calculate next guess
 insert a timer to delay comp decisions by 1-2 seconds each time
'''

def gameType():
    gameTypeMsg = str((raw_input("Do you want to GUESS the number or CHOOSE the number? (enter g or c) ")))
    if gameTypeMsg == "c":
        print "coming soon!"
        gameType()
    elif gameTypeMsg == "g":
        newGame()
    else:
        print "Unexpected input"
        gameType()

def makeGuess():
    global countGuess
    while countGuess < noOfGuess:
        print "Guesses remaining: %d " % (noOfGuess - countGuess)
        newGuess = int(raw_input("Enter your guess between %d and %d: " % (lBoundNo, uBoundNo)))
        if newGuess == secAnswer:
            print "Well done - you win!!"
            global noWins
            noWins += 1
            newGame()
        elif newGuess > secAnswer:
            print "Lower!"
        elif newGuess < secAnswer:
            print "Higher!"
        else:
            print "Error - not a number. You lose a guess."
        countGuess += 1
    if countGuess == noOfGuess:
        print "You lose! The secret number was " + str(secAnswer)
        global noLosses
        noLosses += 1
    newGame()

def newGame():
    print "In this session you have " + str(noWins) + " wins and " + str(noLosses) + " losses"
    newGameMsg = str((raw_input("Do you want to play a new game? (y/n , or o for options) ")))
    if newGameMsg == "y":
        # clear all variables
        # calculate new secret answer
        global secAnswer
        global countGuess
        countGuess = 0
        secAnswer = random.randrange(lBoundNo, uBoundNo)
        #print secAnswer
        makeGuess()
    elif newGameMsg == "n":
        raise SystemExit
    elif newGameMsg == "o":
        print "coming soon!"
        newGame()
    else:
        print "Unexpected input"
        newGame()

gameType()
