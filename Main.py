from random import randint
import pygame
from pygame.locals import *
from Classes import *
from copy import deepcopy
import time
globalCounter = 0
# sets up pygame
pygame.init()
# sets up pygame's clock system
clock = pygame.time.Clock()
# sets up the windowed screen and allowing things to resize when window size changed
screen = pygame.display.set_mode((1920, 1080), RESIZABLE, VIDEORESIZE)
WIDTH = 1920
HEIGHT = 1080
width, height = pygame.display.get_surface().get_size()
scaleWidth = width / WIDTH
scaleHeight = height / HEIGHT
Open = True
blankBoard = [
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0],
             [0, 0, 0, 0, 0]
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
    for row in board:
        counter2 = 0
        for Card in row:
            if Card != 0:
                thisSpot = spot[counter1][counter2]
                board[counter1+thisSpot[1] % len(board)][counter2+thisSpot[0] % len(board)] = board[counter1][counter2]
            counter2 += 1
        counter1 += 1
    return board


# will draw all things on the screen
def Draw():
    for row in board:
        for Card in row:
            if Card != 0:
                Card.draw(screen)
    pygame.display.update()


# is called whenever the screen is resized
def reSize(event):
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)
    return width, height, scaleWidth, scaleHeight, screen

while Open:
    # makes sure the game is running no faster than 60 fps
    clock.tick(60)
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
