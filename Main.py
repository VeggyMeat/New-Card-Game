from random import randint
from pygame.locals import *
import pygame
from Cards import *
from Enemies import *
from Classes import *
from Definitions import *
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
stackCards = deck
maxIchor = 4
currentEnemy = enemies[0]
currentEnemy.resize(scaleWidth, scaleHeight)
ichorLeft = maxIchor
hp = 100
cardsDRAWN = 10

# all the blank templates for moving cards, the board

blankCard = {'card': False, 'playable': False, 'attacked': 0, 'spores': 0, 'block': 0}

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
for x in range(5):
    for y in range(5):
        if randint(0, 1) == 1:
            board[x][y]['card'] = Card(x, y, 120 * x + 50, 170 * y + 50, cards[0][0], cards[0][1], cards[0][2], cards[0][3], cards[0][4], cards[0][5])
            board[x][y]['card'].resize(scaleWidth, scaleHeight)


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
    screen.fill(WHITE)
    for row in board:
        for card in row:
            if card['card'] != False:
                card['card'].draw(screen)
    currentEnemy.draw(screen, globalCounter)
    pygame.display.update()


# is called whenever the screen is resized
def reSize(event):
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)
    for row in board:
        for card in row:
            if card['card'] != False:
                card['card'].resize(scaleWidth, scaleHeight)
    currentEnemy.resize(scaleWidth, scaleHeight)
    return width, height, scaleWidth, scaleHeight, screen


def nextTurn():
    global turn, hp, ichorLeft
    turn += 1
    for row in board:
        for card in row:
            hp -= card['attacked']
    currentEnemy.turn(turn, board, hp)
    ichorLeft = maxIchor


def clicked():
    global ichorLeft, board, currentEnemy
    print(ichorLeft)
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_pos()
    response = True
    if pressed[0]:
        for row in board:
            for card in row:
                if card['card'] != False:
                    if location[0] > card['card'].resizedX and location[0] < card['card'].resizedX + card['card'].resizedImageSize[0]:
                        if location[1] > card['card'].resizedY and location[1] < card['card'].resizedY + card['card'].resizedImageSize[1]:
                            ID = card['card'].id
                            response, ichorLeft, currentEnemy, board = card['card'].use(board, blankBoard, ichorLeft, currentEnemy, scaleWidth, scaleHeight)
                            break
    if response != True:
        time.sleep(.1)
        location = (0, 0)
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                if card['card'] != False:
                    if card['card'].id == ID:
                        location = (counter1, counter2)
                counter2 += 1
            counter1 += 1
        if response == 1:
            stackCards.append(board[location[0]][location[1]]['card'])
        if response >= 1:
            board[location[0]][location[1]]['card'] = False

nextTurn()
while Open:
    # makes sure the game is running no faster than 60 fps
    clock.tick(60)
    globalCounter += 1
    # gets the location of the mouse and whether the mouse has been pressed
    for event in pygame.event.get():
        # checks if the person has tried to close the window and closes the code
        if event.type == QUIT:
            Open = False
        # runs reSize when the window has been resized
        elif event.type == VIDEORESIZE:
            width, height, scaleWidth, scaleHeight, screen = reSize(event)

    clicked()
    Draw()
pygame.quit()
