from Cards import *
from Enemies import *
from Classes import *
from Definitions import *
from Constants import *
from Relics import *
from pygame.locals import *
from copy import deepcopy
import time
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
width, height = pygame.display.get_surface().get_size()
scaleWidth = width / WIDTH
scaleHeight = height / HEIGHT

# setting up some variables
Open = True
CurrentEnemies = []
player = Player(100)
for x in range(5):
    Enemy1 = Enemy(enemies[0][0], enemies[0][1], enemies[0][2], enemies[0][3], enemies[0][4], enemies[0][5], enemies[0][6], enemies[0][7], enemies[0][8], enemies[0][9])
    Enemy1.resize(scaleWidth, scaleHeight)
    CurrentEnemies.append(Enemy1)
cardsDRAWN = 10
previousEnemies = []
CLICKED = False
COUNT = {'enemy': 0, 'card': 0, 'enemies': 0}
TARGET = {'enemy': [], 'card': [], 'enemies': []}
ID = False

# loading some images
SPORES = pygame.transform.scale(pygame.image.load(str(symbolRoot / 'Spore.png')), (10, 10))
RedArrow = pygame.image.load(str(symbolRoot / 'RedArrow.png'))


# all the blank templates for moving cards, the board
blankCard = {'card': False, 'playable': False, 'attacked': {}, 'spores': 0, 'block': 0}
for currentEnemy in CurrentEnemies:
    blankCard['attacked'][str(currentEnemy.id)] = 0

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
            number = randint(6, 6)
            board[x][y]['card'] = Card(x, y, cardGapWIDTH * x + cardSpaceWIDTH, cardGapHEIGHT * y + cardSpaceHEIGHT, cards[number][0], cards[number][1], cards[number][2], cards[number][3], cards[number][4], cards[number][5], cards[number][6])
            board[x][y]['card'].resize(scaleWidth, scaleHeight)


# will draw all things on the screen called every loop
def Draw(random=(True, ())):
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
                pygame.draw.rect(screen, colour, (int((cardGapWIDTH * counter1 + cardSpaceWIDTH - 5) * scaleWidth) + 1, int((cardGapHEIGHT * counter2 + cardSpaceHEIGHT - 5) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card']:
                    # changes the text in the card to the opposite of the background
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * cardGapWIDTH + cardSpaceWIDTH) * scaleWidth) + 1, int((counter2 * cardGapHEIGHT + cardSpaceHEIGHT) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            tempAttack = 0
            for currentEnemy in CurrentEnemies:
                tempAttack += card['attacked'][str(currentEnemy.id)]

            if tempAttack > 0:
                # blurs the colour if its playable and attacked
                colour = RED
                if PLACEDCOLOUR:
                    colour = (int((colour[0]+PLACEDCOLOUR[0]) / 2), int((colour[1]+PLACEDCOLOUR[1]) / 2), int((colour[2]+PLACEDCOLOUR[2]) / 2))
                PLACEDCOLOUR = colour

                # draws a rectangle behind the card showing its being attacked
                pygame.draw.rect(screen, colour, (int((cardGapWIDTH * counter1 + cardSpaceWIDTH - 5) * scaleWidth) + 1, int((cardGapHEIGHT * counter2 + cardSpaceHEIGHT - 5) * scaleHeight) + 1, int((cardWIDTH + 10) * scaleWidth) + 1, int((cardHEIGHT + 10) * scaleHeight) + 1))
                if card['card']:
                    # changes the text in the card to the opposite of the background
                    oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                    pygame.draw.rect(screen, oppositeColour, (int((counter1 * cardGapWIDTH + cardSpaceWIDTH) * scaleWidth) + 1, int((counter2 * cardGapHEIGHT + cardSpaceHEIGHT) * scaleHeight) + 1, int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1))

            # draws the spores for each card
            for x in range(card['spores']):
                screen.blit(SPORES, (int((cardGapWIDTH * counter1 + cardSpaceWIDTH + x * 25) * scaleWidth), int((cardGapHEIGHT * counter2 + cardSpaceHEIGHT + cardHEIGHT * 1.05) * scaleHeight)))

            # draws the card on the screen if its not blank
            if card['card']:
                card['card'].draw(screen)
            counter2 += 1
        counter1 += 1

    # sets up the bottom text giving basic details and info
    thing = ''
    for enemy in CurrentEnemies:
        thing += str(enemy.hp) + ' '
    textSurface = myFont.render('Ichor left: ' + str(player.ichorLeft) + ', Turn: ' + str(turn) + ', HP: ' + str(player.hp) + ', Enemy HP: ' + thing, False, BLACK)
    screen.blit(textSurface, (10, height-50))

    # draws all the buttons on screen
    for button in buttons:
        button.draw(screen)

    # draws the enemies with a gap in-between them
    counter = 0
    for currentEnemy in CurrentEnemies:
        if previousEnemies != CurrentEnemies:
            tempX = deepcopy(currentEnemy.x)
            currentEnemy.x += counter
            counter += currentEnemy.width + 20 * scaleWidth
            currentEnemy.resize(scaleWidth, scaleHeight)
            currentEnemy.x = tempX
        currentEnemy.draw(screen, globalCounter)

    # makes an item bigger if hovering over it
    if random[0] == 'card':
        card = board[random[1][0]][random[1][1]]
        pygame.draw.rect(screen, WHITE, (int(card['card'].resizedX - card['card'].resizedImageSize[0] / 2), int(card['card'].resizedY - card['card'].resizedImageSize[1] / 2), int(card['card'].resizedImageSize[0] * 2), int(card['card'].resizedImageSize[1] * 2)))
        PLACEDCOLOUR = False
        if card['playable']:
            # draws a rectangle behind the card showing its playable
            colour = FORESTGREEN
            PLACEDCOLOUR = colour
            pygame.draw.rect(screen, colour, (int(card['card'].resizedX - card['card'].resizedImageSize[0] / 2 - 10 * scaleWidth), int(card['card'].resizedY - card['card'].resizedImageSize[1] / 2 - 10 * scaleHeight), int(card['card'].resizedImageSize[0] * 2 + 20 * scaleWidth), int(card['card'].resizedImageSize[1] * 2 + 20 * scaleHeight)))
            if card['card']:
                # changes the text in the card to the opposite of the background
                oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                pygame.draw.rect(screen, oppositeColour, (int(card['card'].resizedX - card['card'].resizedImageSize[0] / 2), int(card['card'].resizedY - card['card'].resizedImageSize[1] / 2), int(card['card'].resizedImageSize[0] * 2), int(card['card'].resizedImageSize[1] * 2)))

        tempAttack = 0
        for currentEnemy in CurrentEnemies:
            tempAttack += card['attacked'][str(currentEnemy.id)]

        if tempAttack > 0:
            # blurs the colour if its playable and attacked
            colour = RED
            if PLACEDCOLOUR != False:
                colour = (int((colour[0] + PLACEDCOLOUR[0]) / 2), int((colour[1] + PLACEDCOLOUR[1]) / 2), int((colour[2] + PLACEDCOLOUR[2]) / 2))

            # draws a rectangle behind the card showing its being attacked
            pygame.draw.rect(screen, colour, (int(card['card'].resizedX - card['card'].resizedImageSize[0] / 2 - 10 * scaleWidth), int(card['card'].resizedY - card['card'].resizedImageSize[1] / 2 - 10 * scaleHeight), int(card['card'].resizedImageSize[0] * 2 + 20 * scaleWidth), int(card['card'].resizedImageSize[1] * 2 + 20 * scaleHeight)))
            if card['card'] != False:
                # changes the text in the card to the opposite of the background
                oppositeColour = (255 - colour[0], 255 - colour[1], 255 - colour[2])
                pygame.draw.rect(screen, oppositeColour, (int(card['card'].resizedX - card['card'].resizedImageSize[0] / 2), int(card['card'].resizedY - card['card'].resizedImageSize[1] / 2), int(card['card'].resizedImageSize[0] * 2), int(card['card'].resizedImageSize[1] * 2)))
        card = board[random[1][0]][random[1][1]]['card']
        screen.blit(pygame.transform.scale(card.resizedImage, (int(card.resizedImageSize[0] * 2), int(card.resizedImageSize[1] * 2))), (int(card.resizedX - card.resizedImageSize[0] / 2), int(card.resizedY - card.resizedImageSize[1] / 2)))

    if random[0] == 'enemy':
        enemy = CurrentEnemies[random[1]]
        # pygame.draw.rect(screen, WHITE, (int(enemy.resizedX - enemy.resizedImageSize[0] / 2), int(enemy.resizedY - enemy.resizedImageSize[1] / 2), int(enemy.resizedImageSize[0] * 2), int(enemy.resizedImageSize[1] * 2)))
        screen.blit(pygame.transform.scale(enemy.resizedImages[int(globalCounter / 10) % len(enemy.resizedImages)], (enemy.resizedImageSize[0] * 2, enemy.resizedImageSize[1] * 2)), (int(enemy.resizedX - enemy.resizedImageSize[0] / 2), int(enemy.resizedY - enemy.resizedImageSize[1] / 2)))

        counter = 0
        for symbol in enemy.resizedSymbols:
            screen.blit(symbol, (enemy.resizedX + int(counter * enemy.resizedSymbolSize[0]), int(enemy.resizedY + enemy.resizedImageSize[1] + enemy.resizedSymbolSize[1])))
            counter += 1.2

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
            if card['card']:
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
    global turn, hp, board, player

    # calls any relics with the tag endTurn
    for relic in player.relics:
        call = False
        for item in relic.activated:
            if item == 'endTurn':
                call = True
                break
        if call:
            board, player = relic.definition(board, player)

    # attacks for each enemy
    for currentEnemy in CurrentEnemies:
        player.hp, board = currentEnemy.attack(currentEnemy, turn, board, player.hp)

    # does the poison stuff
    for currentEnemy in CurrentEnemies:
        if currentEnemy.poison > 0:
            currentEnemy.hp -= round(currentEnemy.poison / 2)
            currentEnemy.poison -= 1

    if player.poison > 0:
        player.hp -= round(player.poison / 2)
        player.poison -= 1

    # increases turn counter
    turn += 1

    # starts a loop taking any damage directed at the board and checks whether theres a card and
    counter = 0
    for row in board:
        for card in row:
            if card['block'] > 0:
                print(card['block'], card['attacked'])
            for id in card['attacked']:
                if card['attacked'][str(id)] - card['block'] > 0:
                    player.totalBlock -= card['attacked'][id] - card['block']
                card['attacked'][str(id)] = 0
            card['block'] = 0
            if card['card']:
                player.stackCards.append(card['card'])
                counter += 1
                card['card'] = False
    
    # removes player block
    if player.totalBlock < 0:
        player.hp += player.totalBlock
    player.totalBlock = 0

    # draws cards out of the deck and places them on the board
    for x in range(len(player.stackCards)):
        board, player.stackCards = drawCard(board, player.stackCards)

    # gives each enemy his turn showing where he will attack
    for currentEnemy in CurrentEnemies:
        board = currentEnemy.turn(turn, board)

    # resets ichor and reSizes for any new cards or enemies
    player.ichorLeft = player.maxIchor
    event = Mouse()
    event.w, event.h = width, height
    reSize(event)


# gets run to check if anything has been clicked
def clicked():
    # globals in some variables
    global player, board, CurrentEnemies, globalCounter, Open, scaleWidth, scaleHeight, SPORES, width, height, screen, RedArrow, random, CLICKED, ID, TARGET, COUNT

    # updates mouse and sets a variable checking if i get a response
    pressed = pygame.mouse.get_pressed()
    location = pygame.mouse.get_pos()

    # sets up a loop and goes through each card
    counter1 = 0
    for row in board:
        counter2 = 0
        for card in row:
            # checks if the spot is filled by a card
            if card['card']:
                # checks if someone has hovered over the card
                if card['card'].resizedX < location[0] < card['card'].resizedX + card['card'].resizedImageSize[0]:
                    if card['card'].resizedY < location[1] < card['card'].resizedY + card['card'].resizedImageSize[1]:
                        # checks if the button has been pressed
                        if pressed[0]:
                            if not CLICKED:
                                CLICKED = card
                                ID = card['card'].id
                                if CLICKED['card'].select['enemies'] == 1:
                                    TARGET['enemies'] = CurrentEnemies
                                    COUNT['enemies'] += 1
                            elif COUNT['card'] != CLICKED['card'].select:
                                TARGET['card'].append(card)
                        else:
                            # gets ready to draw the card bigger
                            random = ('card', (counter1, counter2))
            counter2 += 1
        counter1 += 1
    if CLICKED:
        if COUNT == CLICKED['card'].select:
            response, player.ichorLeft, TARGET, board = CLICKED['card'].use(board, blankBoard, TARGET, scaleWidth, scaleHeight, turn, player, CurrentEnemies)
            # loops through each card
            counter1 = 0
            for row in board:
                counter2 = 0
                for card in row:
                    # if there is an actual card there than it checks its id to match the one taken previously and saves its location
                    if card['card']:
                        if card['card'].id == ID:
                            location = (counter1, counter2)
                    counter2 += 1
                counter1 += 1

            board[location[0]][location[1]]['card'] = CLICKED['card']

            # based on the card's response remove the card or remove and add it back to the deck
            if response == 1:
                player.stackCards.append(board[location[0]][location[1]]['card'])
            if response >= 1:
                board[location[0]][location[1]]['card'] = False
            TARGET = {'enemy': [], 'card': [], 'enemies': []}
            CLICKED = False
            COUNT = {'enemy': 0, 'card': 0, 'enemies': 0}

    # if the escape key has been pressed it leaves the
    if pygame.key.get_pressed()[K_ESCAPE]:
        CLICKED = False

    # shows if you have selected an enemy
    counter = 0
    for currentEnemy in CurrentEnemies:
        if currentEnemy.resizedX < location[0] < currentEnemy.resizedX + currentEnemy.resizedImageSize[0]:
            if currentEnemy.resizedY < location[1] < currentEnemy.resizedY + currentEnemy.resizedImageSize[1]:
                random = ('enemy', counter)
                if pressed[0]:
                    if CLICKED:
                        if CLICKED['card'].select['enemy'] != COUNT['enemy']:
                            TARGET['enemy'].append(currentEnemy)
                            COUNT['enemy'] += 1
        counter += 1

    # checks if any of the buttons have been pressed and if so calls its definition
    if pressed[0]:
        for button in buttons:
            if button.resizedX < location[0] < button.resizedX + button.resizedWidth:
                if button.resizedY < location[1] < button.resizedY + button.resizedHeight:
                    button.use()
                    # tries to stop someone accidentally selecting a button immediately after because of holding down the mouse
                    time.sleep(.15)


nextTurnButton = Button(WIDTH-100, HEIGHT-20, 100, 20, nextTurn, RED)
buttons = [nextTurnButton]
nextTurn()
random = (False, ())
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
    random = (False, ())
pygame.quit()
