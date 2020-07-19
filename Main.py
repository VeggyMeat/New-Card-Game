from random import randint
import pygame
from pygame.locals import *
from Classes import *
import time
# sets up pygame
pygame.init()
# sets up pygame's clock system
clock = pygame.time.Clock()
# sets up the windowed screen and allowing things to resize when window size changed
globalCounter = 0
screen = pygame.display.set_mode((1920, 1080), RESIZABLE, VIDEORESIZE)
WIDTH = 1920
HEIGHT = 1080
Open = True




# some code to shuffle a deck of cards
def shuffle(deck):
    newDeck = []
    while len(deck) > 0:
        card = deck[randint(1, len(deck)-1)]
        newDeck.append(card)
        deck.remove(card)


# will draw all things on the screen
def Draw():
    pass


# is called whenever the screen is resized
def reSize():
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)


reSize()
while Open:
    # makes sure the game is running no faster than 60 fps
    clock.tick(60)
    # gets the location of the mouse and whether the mouse has been pressed
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_cursor()
    for event in pygame.event.get():
        # checks if the person has tried to close the window and closes the code
        if event.type == event.QUIT:
            Open = False
        # runs reSize when the window has been resized
        elif event.type == event.VIDEORESIZE:
            reSize()

    Draw()
pygame.quit()
