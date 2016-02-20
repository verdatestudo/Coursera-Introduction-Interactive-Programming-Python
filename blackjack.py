'''
An Introduction to Interactive Programming in Python - week 6
Blackjack
2015-Nov-29
Python 2.7
Chris
'''

import simplegui
import random

# canvas size
canvasHeight = 600
canvasWidth = 600

leftPos = 50 # position for the leftmost card

# load card sprite - 936x384 - source: jfitz.com
CARD_SIZE = (72, 96)
CARD_CENTER = (36, 48)
card_images = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/cards_jfitz.png")
# card back sizes (144 x 96, half is 72 x 48)
CARD_BACK_SIZE = (72, 96)
CARD_BACK_CENTER = (36, 48)
card_back = simplegui.load_image("http://storage.googleapis.com/codeskulptor-assets/card_jfitz_back.png")

# initialize some useful global variables
in_play = False
outcome = ""
score = 0
consoleMsg = ""

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}


# define card class
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        return self.suit + self.rank

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank

    def draw(self, canvas, pos):
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank),
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE, [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]], CARD_SIZE)

# define hand class
class Hand:
    def __init__(self):
        self.listCards = []	# create Hand object

    def __str__(self):
        ans = ""
        for i in range(len(self.listCards)):
            ans += Card.get_suit(self.listCards[i])
            ans += Card.get_rank(self.listCards[i]) + " "
        return ans
        # return a string representation of a hand

    def add_card(self, card):
        self.listCards.append(card)
        # add a card object to a hand

    def get_value(self):
        value = 0
        aceCount = 0
        for card in self.listCards:
            if card.get_rank() == 'A':
                aceCount += 1
            value += VALUES[card.get_rank()]
        if value < 12 and aceCount > 0:
            value += 10
        return value

        # count aces as 1, if the hand has an ace, then add 10
        # to hand value if it doesn't bust
        # compute the value of the hand, see Blackjack video

    def draw(self, canvas, pos):
        # draw a hand on the canvas, use the draw method for cards
        for card in self.listCards:
            card.draw(canvas, pos)
            pos[0] += 100

# define deck class
class Deck:

    def __init__(self):
        self.listCards = []
        for suit in SUITS:
            for rank in RANKS:
                self.listCards.append(Card(suit, rank))
        # create a Deck object


    def shuffle(self):
        # shuffle the deck
        random.shuffle(self.listCards)
        # use random.shuffle()

    def deal_card(self):
        dealtCard = self.listCards.pop()
        return dealtCard
        # deal a card object from the deck

    def __str__(self):
        ans = ""
        for i in range(len(self.listCards)):
            ans += Card.get_suit(self.listCards[i])
            ans += Card.get_rank(self.listCards[i]) + " "
        return ans
        pass	# return a string representing the deck


#define event handlers for buttons
def deal():
    global score, outcome, in_play, currentDeck, playerHand, dealerHand, consoleMsg

    if in_play == True:
        consoleMsg = "You forfeit"
        winResult('d')
    else:
        consoleMsg = "Hit or stand?"
        in_play = True
        currentDeck = Deck()
        playerHand = Hand()
        dealerHand = Hand()
        currentDeck.shuffle()
        playerHand.add_card(currentDeck.deal_card())
        dealerHand.add_card(currentDeck.deal_card())
        playerHand.add_card(currentDeck.deal_card())
        dealerHand.add_card(currentDeck.deal_card())

        if dealerHand.get_value() == 21:
            consoleMsg = "Blackjack!"
            winResult('d')
        elif playerHand.get_value() == 21:
            stand()
    # your code goes here


def hit():

    global in_play, playerHand, currentDeck

    if in_play == False:
        return

    if playerHand.get_value() < 21:
        playerHand.add_card(currentDeck.deal_card())

    if playerHand.get_value() == 21:
        stand()

    if playerHand.get_value() > 21:
        checkResult()

    # if the hand is in play, hit the player
    # if busted, assign a message to outcome, update in_play and score

def stand():

    global in_play, playerHand, dealerHand, currentDeck

    if in_play == False:
        return

    if dealerHand.get_value > 16:
        checkResult()

    while dealerHand.get_value() < 17:
        dealerHand.add_card(currentDeck.deal_card())

    checkResult()

    # if hand is in play, repeatedly hit dealer until his hand has value 17 or more
    # assign a message to outcome, update in_play and score

# draw handler
def draw(canvas):
    # test to make sure that card.draw works, replace with your code below
    # card = Card("S", "A")
    # card.draw(canvas, [pos, canvasHeight - 200])
    canvas.draw_text('# BLACKJACK #', [100, 50], 52, 'Black')
    canvas.draw_text('The score is ... ' + str(score), [50, 300], 20, 'blue')
    canvas.draw_text('Player hand = ' + str(playerHand.get_value()), [100, 400], 20, 'pink')
    playerHand.draw(canvas, [leftPos, canvasHeight - 150])
    dealerHand.draw(canvas, [leftPos, 150])
    canvas.draw_text(str(consoleMsg), [300, 300], 20, 'Red')
    if in_play == True:
        canvas.draw_image(card_back, (CARD_BACK_CENTER), (CARD_BACK_SIZE), (leftPos+CARD_BACK_SIZE[0]/2, 150+CARD_BACK_SIZE[1]/2), (CARD_SIZE), 0)
    if in_play == False:
        canvas.draw_text('Dealer hand = ' + str(dealerHand.get_value()), [100, 350], 20, 'pink')


def checkResult():
    global in_play, consoleMsg
    in_play = False
    difValue = playerHand.get_value() - dealerHand.get_value()
    if playerHand.get_value() > 21:
        consoleMsg = "Player has busted"
        winResult('d')
    elif dealerHand.get_value() > 21:
        consoleMsg = "Dealer has busted"
        winResult('p')
    elif difValue > 0:
        winResult('p')
    else:
        winResult('d')

def winResult(name):
    global in_play, score, consoleMsg
    in_play = False

    if name == 'd':
        score -= 1
        consoleMsg = "Dealer is the winner. New game?"
    elif name == 'p':
        score += 1
        consoleMsg = "Player is the winner. New game?"
    else:
        print "Error!!!"

# initialization frame
frame = simplegui.create_frame("Blackjack", canvasWidth, canvasHeight)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.set_draw_handler(draw)
#timer = simplegui.create_timer(3000, timerStop)

# get things rolling
deal()

frame.start()



# remember to review the gradic rubric
