from random import randint
import pygame
from pygame.locals import *
from Classes import *
from Cards import *
from copy import deepcopy
import time
globalCounter = 0
turn = 0
# sets up pygame
pygame.init()
# sets up pygame's clock system
clock = pygame.time.Clock()
# basic colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
TURQUOISE = (0, 255, 255)
YELLOW = (0, 255, 255)
ORANGE = (255, 128, 0)
# sets up the windowed screen and allowing things to resize when window size changed
screen = pygame.display.set_mode((1920, 1080), RESIZABLE, VIDEORESIZE)
WIDTH = 1920
HEIGHT = 1080
cardWIDTH = 100
cardHEIGHT = 150
width, height = pygame.display.get_surface().get_size()
scaleWidth = width / WIDTH
scaleHeight = height / HEIGHT
Open = True
deck = []
maxIchor = 4
currentEnemy = 0
ichorLeft = maxIchor
hp = 100

# all the blank templates for moving cards, the board

blankCard = {'card': False, 'playable': False, 'attacked': 0, 'effects': {'spores': 0, 'block': 0}}

blankBoard = [
              [deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard)],
              [deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard)],
              [deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard)],
              [deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard)],
              [deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard), deepcopy(blankCard)]
             ]

blankMove = [
             [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
             [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
             [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
             [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)],
             [(0, 0), (0, 0), (0, 0), (0, 0), (0, 0)]
            ]

board = deepcopy(blankBoard)


# some code to shuffle a deck of cards
def shuffle(deck):
    newDeck = []
    while len(deck) > 0:
        card = deck[randint(1, len(deck)-1)]
        newDeck.append(card)
        deck.remove(card)
    return newDeck


# code to allow two arrays to be entered with one being the board and the other where each card moves on a co-ordinate system and moves each one and allows them to loop
def move(board, spot):
    counter1 = 0
    newBoard = deepcopy(blankBoard)
    for row in board:
        counter2 = 0
        for card in row:
            if not card['card']:
                thisSpot = spot[counter1][counter2]
                newBoard[(counter1+thisSpot[0]) % len(board)][(counter2+thisSpot[1]) % len(board)] = board[counter1][counter2]
            counter2 += 1
        counter1 += 1
    return newBoard


# will draw all things on the screen
def Draw():
    for row in board:
        for card in row:
            if not card['card']:
                card['card'].draw(screen)
    pygame.display.update()


# is called whenever the screen is resized
def reSize(event):
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)
    return width, height, scaleWidth, scaleHeight, screen


def nextTurn(currentEnemy):
    global turn, ichorLeft, hp
    turn += 1
    for row in board:
        for card in row:
            hp -= card['attacked']
    currentEnemy.turn()
    ichorLeft = maxIchor


nextTurn(currentEnemy)
while Open:
    # makes sure the game is running no faster than 60 fps
    clock.tick(60)
    globalCounter += 1
    # gets the location of the mouse and whether the mouse has been pressed
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_cursor()
    for event in pygame.event.get():
        # checks if the person has tried to close the window and closes the code
        if event.type == QUIT:
            Open = False
        # runs reSize when the window has been resized
        elif event.type == VIDEORESIZE:
            width, height, scaleWidth, scaleHeight, screen = reSize(event)

    Draw()
pygame.quit()
