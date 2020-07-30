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

# setting up some variables
Open = True
deck = []
stackCards = deck
maxIchor = 5
CurrentEnemies = []
for x in range(5):
    Enemy1 = Enemy(enemies[0][0], enemies[0][1], enemies[0][2], enemies[0][3], enemies[0][4], enemies[0][5], enemies[0][6], enemies[0][7], enemies[0][8], enemies[0][9])
    Enemy1.resize(scaleWidth, scaleHeight)
    CurrentEnemies.append(Enemy1)
ichorLeft = maxIchor
hp = 100
cardsDRAWN = 10
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

# makes a copy of blankBoard for the board
board = deepcopy(blankBoard)

# sets up four random playable squares
for x in range(4):
    while True:
        number = (randint(0, 4), randint(0, 4))
        if not board[number[0]][number[1]]['playable']:
            board[number[0]][number[1]]['playable'] = True
            break

# sets up some random cards
for x in range(5):
    for y in range(5):
        if randint(0, 1) == 1:
            number = randint(0, 3)
            board[x][y]['card'] = Card(x, y, 120 * x + 50, 170 * y + 50, cards[number][0], cards[number][1], cards[number][2], cards[number][3], cards[number][4], cards[number][5], cards[number][6])
            board[x][y]['card'].resize(scaleWidth, scaleHeight)


# code to allow two arrays to be entered with one being the board and the other where each card moves on a co-ordinate system and moves each one and allows them to loop
def move(board, spot):
    # makes a blank board
    newBoard = deepcopy(blankBoard)

    # starts a loop with some counters
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            # if the card is an actual card then move it to the same place but adds the spot
            if card['card'] != False:
                thisSpot = spot[counter1][counter2]
                newBoard[(counter1+thisSpot[0]) % len(board)][(counter2+thisSpot[1]) % len(board)] = board[counter1][counter2]
            counter2 += 1
        counter1 += 1

    # returns the newly made board
    return newBoard


# will draw all things on the screen called every loop
def Draw(random=True):
    # globals in some variables
    global scaleWidth, scaleHeight, previousEnemies, screen

    # fills the screen white
    screen.fill((WHITE))

    # starts a massive loop with counters going through each card
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            # sets a variable to blur colours if placed over each other for backgrounds of the cards
            PLACEDCOLOUR = False
            if card['playable']:
                # draws a rectangle behind the card showing its playable
                colour = FORESTGREEN
                PLACEDCOLOUR = colour
                pygame.draw.rect(screen, colour, (int((120 * counter1 + 45) * scaleWidth) + 1, int((170 * counter2 + 45) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card'] != False:
                    # changes the text in the card to the opposite of the background
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * 120 + 50) * scaleWidth) + 1, int((counter2 * 170 + 50) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            if card['attacked'] > 0:
                # blurs the colour if its playable and attacked
                colour = RED
                if PLACEDCOLOUR != False:
                    colour = (int((colour[0]+PLACEDCOLOUR[0]) / 2), int((colour[1]+PLACEDCOLOUR[1]) / 2), int((colour[2]+PLACEDCOLOUR[2]) / 2))
                PLACEDCOLOUR = colour

                # draws a rectangle behind the card showing its being attacked
                pygame.draw.rect(screen, colour, (int((120 * counter1 + 45) * scaleWidth) + 1, int((170 * counter2 + 45) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card'] != False:
                    # changes the text in the card to the opposite of the background
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * 120 + 50) * scaleWidth) + 1, int((counter2 * 170 + 50) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            # draws the spores for each card
            for x in range(card['spores']):
                screen.blit(SPORES, (int((120 * counter1 + 50 + x * 25) * scaleWidth), int((170 * counter2 + 50 + cardHEIGHT * 1.05) * scaleHeight)))

            # draws the card on the screen if its not blank
            if card['card'] != False:
                card['card'].draw(screen)
            counter2 += 1
        counter1 += 1

    # sets up the bottom text giving basic details and info
    thing = ''
    for enemy in CurrentEnemies:
        thing += str(enemy.hp) + ' '
    textSurface = myFont.render('Ichor left: ' + str(ichorLeft) + ', Turn: ' + str(turn) + ', HP: ' + str(hp) + ', Enemy HP: ' + thing, False, BLACK)
    screen.blit(textSurface, (10, height-50))

    # draws all the buttons on screen
    for button in buttons:
        button.draw(screen)

    # draws the enemies with a gap inbetween them
    counter = 0
    for currentEnemy in CurrentEnemies:
        if previousEnemies != CurrentEnemies:
            tempX = deepcopy(currentEnemy.x)
            currentEnemy.x += counter
            counter += currentEnemy.width + 20 * scaleWidth
            currentEnemy.resize(scaleWidth, scaleHeight)
            currentEnemy.x = tempX
        currentEnemy.draw(screen, globalCounter)

    # draws an arrow above something if needed
    if random != True:
        screen.blit(RedArrow, (random[0], random[1]))

    # updates screen
    pygame.display.update()


# is called whenever the screen is resized
def reSize(event):
    # globals in some variables
    global SPORES, RedArrow

    # sets up variables
    width = event.w
    height = event.h
    scaleWidth = width / WIDTH
    scaleHeight = height / HEIGHT
    screen = pygame.display.set_mode((width, height), RESIZABLE, VIDEORESIZE)

    # resizes a couple of images
    SPORES = pygame.transform.scale(SPORES, (int(10 * scaleWidth), int(10 * scaleHeight)))
    RedArrow = pygame.transform.scale(RedArrow, (int(25 * scaleWidth), int(25 * scaleHeight)))

    # resizes every card
    for row in board:
        for card in row:
            if card['card'] != False:
                card['card'].resize(scaleWidth, scaleHeight)

    # resizes all the buttons
    for button in buttons:
        button.resize(scaleWidth, scaleHeight)

    # resizes all the enemies
    for currentEnemy in CurrentEnemies:
        currentEnemy.resize(scaleWidth, scaleHeight)
    return width, height, scaleWidth, scaleHeight, screen


# is ran whenever it goes to the next turn
def nextTurn():
    # globals in some variables
    global turn, hp, ichorLeft, board, stackCards

    # attacks for each enemy
    for currentEnemy in CurrentEnemies:
        hp, board = currentEnemy.attack(currentEnemy, turn, board, hp)

    # increases turn counter
    turn += 1

    # starts a loop taking any damage directed at the board and checks whether theres a card and
    counter = 0
    for row in board:
        for card in row:
            hp -= card['attacked']
            card['attacked'] = 0
            if card['card'] != False:
                stackCards.append(card['card'])
                counter += 1
                card['card'] = False

    # draws cards out of the deck and places them on the board
    for x in range(len(stackCards)):
        board, stackCards = drawCard(board, stackCards)

    # gives each enemy his turn showing where he will attack
    for currentEnemy in CurrentEnemies:
        board = currentEnemy.turn(turn, board)

    # resets ichor and reSizes for any new cards or enemies
    ichorLeft = maxIchor
    event = Mouse()
    event.w, event.h = width, height
    reSize(event)


# gets run to check if anything has been clicked
def clicked():
    # globals in some variables
    global ichorLeft, board, CurrentEnemies, globalCounter, Open, scaleWidth, scaleHeight, SPORES, width, height, screen, RedArrow, random

    # updates mouse and sets a variable checking if i get a response
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_pos()
    response = 'a'

    # sets up a loop and goes through each card
    for row in board:
        for card in row:
            # checks if the spot is filled by a card
            if card['card'] != False:
                # checks if someone has hovered over the card
                if card['card'].resizedX < location[0] < card['card'].resizedX + card['card'].resizedImageSize[0]:
                    if card['card'].resizedY < location[1] < card['card'].resizedY + card['card'].resizedImageSize[1]:
                        # gets ready to draw a red arrow over the highlited card
                        random = (card['card'].resizedX + int(card['card'].resizedImageSize[0] / 2)- int(12*scaleWidth), card['card'].resizedY - int(30*scaleHeight))

                        # checks if the button has been pressed
                        if pressed[0]:
                            # notes down the id of the card so it can be removed if it isn't played
                            ID = card['card'].id

                            # gets some variables ready for the loop which is ran if the card needs to know what thing to select
                            enemy = CurrentEnemies
                            escape = False
                            leave = False
                            random = True
                            while card['card'].select:
                                # imitates the main loop inside of this so the screen still updates
                                clock.tick(60)
                                Draw(random)
                                random = True
                                globalCounter += 1
                                pressed = pygame.mouse.get_pressed()
                                location = pygame.mouse.get_pos()
                                # checks if one of the enemies gets hovered over and selected
                                for currentEnemy in CurrentEnemies:
                                    if currentEnemy.resizedX < location[0] < currentEnemy.resizedX + currentEnemy.resizedImageSize[0]:
                                        if currentEnemy.resizedY < location[1] < currentEnemy.resizedY + currentEnemy.resizedImageSize[1]:
                                            random = (currentEnemy.resizedX + int(currentEnemy.resizedImageSize[0] / 2)- int(12*scaleWidth), currentEnemy.resizedY - int(30*scaleHeight))
                                            if pressed[0]:
                                                enemy = currentEnemy
                                                leave = True

                                # looks through the pygame events
                                for event in pygame.event.get():
                                    # checks if the person has tried to close the window and closes the code
                                    if event.type == QUIT:
                                        Open = False
                                    # runs reSize when the window has been resized
                                    elif event.type == VIDEORESIZE:
                                        SPORES = pygame.transform.scale(SPORES, (int(10 * scaleWidth), int(10 * scaleHeight)))
                                        width, height, scaleWidth, scaleHeight, screen = reSize(event)

                                # if the escape key has been pressed it leaves the loop
                                if pygame.key.get_pressed()[K_ESCAPE]:
                                    escape = True

                                # breaks the loop if one of the conditions is met
                                if not Open or escape or leave:
                                    break

                            # if the game is still true and the playing of the card hasn't been cancelled then play the card
                            if Open and not escape:
                                response, ichorLeft, enemy, board = card['card'].use(board, blankBoard, ichorLeft, enemy, scaleWidth, scaleHeight, turn)

                                # tries to stop someone accidentally selecting a card immediately after because of holding down the mouse
                                time.sleep(.15)
                            break

    # checks if any of the buttons have been pressed and if so calls its definition
    if pressed[0]:
        for button in buttons:
            if button.resizedX < location[0] < button.resizedX + button.resizedWidth:
                if button.resizedY < location[1] < button.resizedY + button.resizedHeight:
                    button.use()
                    # tries to stop someone accidentally selecting a button immediately after because of holding down the mouse
                    time.sleep(.15)

    # if the card was actually played then this runs
    if response != 'a':
        # loops through each card
        counter1 = 0
        for row in board:
            counter2 = 0
            for card in row:
                # if there is an actual card there than it checks its id to match the one taken previously and saves its location
                if card['card'] != False:
                    if card['card'].id == ID:
                        location = (counter1, counter2)
                counter2 += 1
            counter1 += 1

        # based on the card's response remove the card or remove and add it back to the deck
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
