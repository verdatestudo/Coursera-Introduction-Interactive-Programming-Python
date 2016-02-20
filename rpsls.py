'''
An Introduction to Interactive Programming in Python - Week 1
Rock-paper-scissors-lizard-Spock
2015-Nov-20
Python 2.7
Chris
'''

# The key idea of this program is to equate the strings
# "rock", "paper", "scissors", "lizard", "Spock" to numbers
# as follows:
#
# 0 - rock
# 1 - Spock
# 2 - paper
# 3 - lizard
# 4 - scissors

import random

# helper functions

def name_to_number(name):
    # delete the following pass statement and fill in your code below

    # convert name to number using if/elif/else
    # don't forget to return the result!

    if name == "rock":
        number = 0
    elif name == "Spock":
        number = 1
    elif name == "paper":
        number = 2
    elif name == "lizard":
        number = 3
    elif name == "scissors":
        number = 4
    else:
        print "Error"

    return number


def number_to_name(number):
    # delete the following pass statement and fill in your code below

    # convert number to a name using if/elif/else
    # don't forget to return the result!

    if number == 0:
        name = "rock"
    elif number == 1:
        name = "Spock"
    elif number == 2:
        name = "paper"
    elif number == 3:
        name = "lizard"
    elif number == 4:
        name = "scissors"
    else:
        print "Error"

    return name



def rpsls(player_choice):
    # delete the following pass statement and fill in your code below

    # print a blank line to separate consecutive games
    print " "
    # print out the message for the player's choice
    print "Player has chosen " + player_choice
    # convert the player's choice to player_number using the function name_to_number()
    playerNumber = name_to_number(player_choice)
    # compute random guess for comp_number using random.randrange()
    compNumber = random.randrange(0,5)
    # convert comp_number to comp_choice using the function number_to_name()
    compChoice = number_to_name(compNumber)
    # print out the message for computer's choice
    print "Computer has chosen " + compChoice
    # compute difference of comp_number and player_number modulo five
    resultNo = compNumber - playerNumber
    if resultNo < 0:
        resultNo += 5
    # use if/elif/else to determine winner, print winner message
    if resultNo == 0:
        print "DRAW"
    elif resultNo == 1 or resultNo == 2:
        print "COMP WIN"
    elif resultNo == 3 or resultNo == 4:
        print "PLAYER WIN"
    else:
        print "ERROR"

# test your code - THESE CALLS MUST BE PRESENT IN YOUR SUBMITTED CODE
rpsls("rock")
rpsls("Spock")
rpsls("paper")
rpsls("lizard")
rpsls("scissors")

# always remember to check your completed program against the grading rubric
