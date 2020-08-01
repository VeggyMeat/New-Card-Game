from random import randint
from Constants import *


# some code to shuffle a deck of cards
def shuffle(deck):
    # makes an empty list
    newDeck = []

    # takes each card in the deck and places each card randomly into the new deck
    while len(deck) > 0:
        card = deck[randint(0, len(deck)-1)]
        newDeck.append(card)
        deck.remove(card)

    # returns the new deck
    return newDeck


# draws a card from the deck places it randomly on the board and removes it from the stack
def drawCard(board, stackCards):
    # shuffles the deck
    stackCards = shuffle(stackCards)

    # makes a loop
    counter = 0
    while True:
        counter += 1
        # creates a failsafe in case every tile is filled
        if counter > 1000:
            break

        # makes a random co-ordinate spot
        cords = (randint(0, 4), randint(0, 4))

        # checks if the spot is empty
        if not board[cords[0]][cords[1]]['card']:
            # places the card and resize it to that spot
            board[cords[0]][cords[1]]['card'] = stackCards[0]
            board[cords[0]][cords[1]]['card'].x, board[cords[0]][cords[1]]['card'].y, board[cords[0]][cords[1]]['card'].screenX, board[cords[0]][cords[1]]['card'].screenY = cords[0], cords[1], cords[0] * cardGapWIDTH + cardSpaceWIDTH, cords[1] * cardGapHEIGHT + cardSpaceHEIGHT
            stackCards.pop(0)
            break
    return board, stackCards
