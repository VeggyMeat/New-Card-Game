from Constants import *
from random import randint
from copy import deepcopy


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
    try:
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
    except IndexError:
        pass
    return board, stackCards


# code to allow two arrays to be entered with one being the board and the other where each card moves on a co-ordinate system and moves each one and allows them to loop
def move(board, spot, blankBoard):
    # makes a blank board
    newBoard = deepcopy(blankBoard)

    # starts a loop with some counters
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            # if the card is an actual card then move it to the same place but adds the spot
            if card['card']:
                thisSpot = spot[counter1][counter2]
                newBoard[(counter1+thisSpot[0]) % len(board)][(counter2+thisSpot[1]) % len(board)] = board[counter1][counter2]
            counter2 += 1
        counter1 += 1

    # returns the newly made board
    return newBoard
