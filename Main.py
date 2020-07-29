from random import randint
from pygame.locals import *
import pygame
from Cards import *
from Enemies import *
from Classes import *
from Definitions import *
from copy import deepcopy
import time
import keyboard
globalCounter = 0
turn = 0
# sets up pygame
pygame.init()
pygame.font.init()
myFont = pygame.font.SysFont('sitkasmallsitkatextbolditalicsitkasubheadingbolditalicsitkaheadingbolditalicsitkadisplaybolditalicsitkabannerbolditalic', 30, False, False)
# sets up pygame's clock system
clock = pygame.time.Clock()
# basic colours
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
FORESTGREEN = (1, 68, 33)
BLUE = (0, 0, 255)
PURPLE = (255, 0, 255)
TURQUOISE = (0, 255, 255)
YELLOW = (255, 255, 0)
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
maxIchor = 5
Enemy1 = Enemy(enemies[0][0], enemies[0][1], enemies[0][2], enemies[0][3], enemies[0][4], enemies[0][5], enemies[0][6], enemies[0][7], enemies[0][8], enemies[0][9])
Enemy1.resize(scaleWidth, scaleHeight)
Enemy2 = Enemy(enemies[0][0], enemies[0][1], enemies[0][2], enemies[0][3], enemies[0][4], enemies[0][5], enemies[0][6], enemies[0][7], enemies[0][8], enemies[0][9])
Enemy2.resize(scaleWidth, scaleHeight)
ichorLeft = maxIchor
hp = 100
cardsDRAWN = 10
CurrentEnemies = [Enemy1, Enemy2]
previousEnemies = []
# loading some images
SPORES = pygame.transform.scale(pygame.image.load(str(symbolRoot / 'Spore.png')), (10, 10))
RedArrow = pygame.image.load(str(symbolRoot / 'RedArrow.png'))


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
for x in range(4):
    while True:
        number = (randint(0, 4), randint(0, 4))
        if not board[number[0]][number[1]]['playable']:
            board[number[0]][number[1]]['playable'] = True
            break
for x in range(5):
    for y in range(5):
        if randint(0, 1) == 1:
            number = randint(2, 3)
            board[x][y]['card'] = Card(x, y, 120 * x + 50, 170 * y + 50, cards[number][0], cards[number][1], cards[number][2], cards[number][3], cards[number][4], cards[number][5], cards[number][6])
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
def Draw(random=True):
    global scaleWidth, scaleHeight, previousEnemies, screen
    screen.fill((WHITE))
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            PLACEDCOLOUR = False
            if card['playable']:
                colour = FORESTGREEN
                PLACEDCOLOUR = colour
                pygame.draw.rect(screen, colour, (int((120 * counter1 + 45) * scaleWidth) + 1, int((170 * counter2 + 45) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card'] != False:
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * 120 + 50) * scaleWidth) + 1, int((counter2 * 170 + 50) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            if card['attacked'] > 0:
                colour = RED
                if PLACEDCOLOUR != False:
                    colour = (int((colour[0]+PLACEDCOLOUR[0]) / 2), int((colour[1]+PLACEDCOLOUR[1]) / 2), int((colour[2]+PLACEDCOLOUR[2]) / 2))
                PLACEDCOLOUR = colour
                pygame.draw.rect(screen, colour, (int((120 * counter1 + 45) * scaleWidth) + 1, int((170 * counter2 + 45) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card'] != False:
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * 120 + 50) * scaleWidth) + 1, int((counter2 * 170 + 50) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            for x in range(card['spores']):
                screen.blit(SPORES, (int((120 * counter1 + 50 + x * 25) * scaleWidth), int((170 * counter2 + 50 + cardHEIGHT * 1.05) * scaleHeight)))

            if card['card'] != False:
                card['card'].draw(screen)
            counter2 += 1
        counter1 += 1
    textSurface = myFont.render('Ichor left: ' + str(ichorLeft) + ', Turn: ' + str(turn) + ', HP: ' + str(hp) + ', Enemy HP: ' + str('huh'), False, BLACK)
    screen.blit(textSurface, (10, height-50))
    for button in buttons:
        button.draw(screen)
    counter = 0
    for currentEnemy in CurrentEnemies:
        if previousEnemies != CurrentEnemies:
            tempX = deepcopy(currentEnemy.x)
            currentEnemy.x += counter
            counter += currentEnemy.width + 20
            currentEnemy.resize(scaleWidth, scaleHeight)
            currentEnemy.x = tempX
        currentEnemy.draw(screen, globalCounter)

    if random != True:
        screen.blit(RedArrow, (random[0], random[1]))

    pygame.display.update()


# is called whenever the screen is resized
def reSize(event):
    global SPORES, RedArrow
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)
    SPORES = pygame.transform.scale(SPORES, (int(10 * scaleWidth), int(10 * scaleHeight)))
    RedArrow = pygame.transform.scale(RedArrow, (int(25 * scaleWidth), int(25 * scaleHeight)))
    for row in board:
        for card in row:
            if card['card'] != False:
                card['card'].resize(scaleWidth, scaleHeight)
    for button in buttons:
        button.resize(scaleWidth, scaleHeight)
    for currentEnemy in CurrentEnemies:
        currentEnemy.resize(scaleWidth, scaleHeight)
    return width, height, scaleWidth, scaleHeight, screen


def nextTurn():
    global turn, hp, ichorLeft, board, stackCards
    for currentEnemy in CurrentEnemies:
        hp, board = currentEnemy.attack(currentEnemy, turn, board, hp)
    turn += 1
    counter = 0
    for row in board:
        for card in row:
            hp -= card['attacked']
            card['attacked'] = 0
            if card['card'] != False:
                stackCards.append(card['card'])
                counter += 1
                card['card'] = False

    for x in range(len(stackCards)):
        board, stackCards = drawCard(board, stackCards)

    for currentEnemy in CurrentEnemies:
        board = currentEnemy.turn(turn, board)
    ichorLeft = maxIchor
    event = Mouse()
    event.w, event.h = width, height
    reSize(event)


def clicked():
    global ichorLeft, board, CurrentEnemies, globalCounter, Open, scaleWidth, scaleHeight, SPORES, width, height, screen, RedArrow, random
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_pos()
    response = 'a'
    for row in board:
        for card in row:
            if card['card'] != False:
                if card['card'].resizedX < location[0] < card['card'].resizedX + card['card'].resizedImageSize[0]:
                    if card['card'].resizedY < location[1] < card['card'].resizedY + card['card'].resizedImageSize[1]:
                        random = (card['card'].resizedX + int(card['card'].resizedImageSize[0] / 2)- int(12*scaleWidth), card['card'].resizedY - int(30*scaleHeight))
                        if pressed[0]:
                            ID = card['card'].id
                            enemy = CurrentEnemies
                            escape = False
                            leave = False
                            random = True
                            while card['card'].select:
                                clock.tick(60)
                                Draw(random)
                                random = True
                                globalCounter += 1
                                pressed = pygame.mouse.get_pressed()
                                location = pygame.mouse.get_pos()
                                for currentEnemy in CurrentEnemies:
                                    if currentEnemy.resizedX < location[0] < currentEnemy.resizedX + currentEnemy.resizedImageSize[0]:
                                        if currentEnemy.resizedY < location[1] < currentEnemy.resizedY + currentEnemy.resizedImageSize[1]:
                                            random = (currentEnemy.resizedX + int(currentEnemy.resizedImageSize[0] / 2)- int(12*scaleWidth), currentEnemy.resizedY - int(30*scaleHeight))
                                            if pressed[0]:
                                                enemy = currentEnemy
                                                leave = True
                                                print('left')
                                for event in pygame.event.get():
                                    # checks if the person has tried to close the window and closes the code
                                    if event.type == QUIT:
                                        Open = False
                                    # runs reSize when the window has been resized
                                    elif event.type == VIDEORESIZE:
                                        SPORES = pygame.transform.scale(SPORES, (int(10 * scaleWidth), int(10 * scaleHeight)))
                                        width, height, scaleWidth, scaleHeight, screen = reSize(event)
                                if pygame.key.get_pressed()[K_ESCAPE]:
                                    escape = True
                                if not Open or escape or leave:
                                    break
                            if Open and not escape:
                                print('ok')
                                response, ichorLeft, enemy, board = card['card'].use(board, blankBoard, ichorLeft, enemy, scaleWidth, scaleHeight, turn)
                                time.sleep(.1)
                            break
    if pressed[0]:
        for button in buttons:
            if button.resizedX < location[0] < button.resizedX + button.resizedWidth:
                if button.resizedY < location[1] < button.resizedY + button.resizedHeight:
                    button.use()
                    time.sleep(.1)

    if response != 'a':
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


nextTurnButton = Button(WIDTH-100, HEIGHT-20, 100, 20, nextTurn, RED)
buttons = [nextTurnButton]
nextTurn()
random = True
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
    counter = 0
    for currentEnemy in CurrentEnemies:
        if currentEnemy.hp <= 0:
            CurrentEnemies.pop(counter)
        counter += 1
    clicked()
    Draw(random)
    random = True
pygame.quit()
