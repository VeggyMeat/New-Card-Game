from random import randint
import pygame
from pathlib import Path
enemies = []
# the root of where the images are
enemyRoot = Path('Images/Enemies/')
symbolRoot = Path('Images/Symbols/')

# some variables
bottomLeft = (900, 900)
sporeDetonation = pygame.image.load(str(symbolRoot / 'SporeDetonation.png'))

# enemies


def MushroomShow(self, turn, board):
    # adds a headbut to a random tile
    board[randint(0, 4)][randint(0, 4)]['attacked'][str(self.id)] += 1

    # gets a probability
    number = randint(1, 4)

    # depending on the probability does anywhere from 1-3 headbutts and 0-4 spores
    if number == 1:
        board[randint(0, 4)][randint(0, 4)]['attacked'][str(self.id)] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
    if number <= 3:
        board[randint(0, 4)][randint(0, 4)]['attacked'][str(self.id)] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1

    # shows that it will blow up the spores if the turn counter is a multiple of 3
    if turn % 3 == 0:
        self.symbols.append(sporeDetonation)
    return board


def MushroomAttack(self, turn, board, hp):
    # if the turn is a multiple of three then it runs
    if turn % 3 == 0 and turn != 0:
        # removes the blow up symbol
        self.symbols.remove(sporeDetonation)

        # loops through each card and deals the numbers of spores damage
        for row in board:
            for card in row:
                hp -= card['spores']
                card['spores'] = 0
    return hp, board


images = [pygame.image.load(str(enemyRoot/'Mushroom1.png')), pygame.image.load(str(enemyRoot/'Mushroom2.png')), pygame.image.load(str(enemyRoot/'Mushroom3.png')), pygame.image.load(str(enemyRoot/'Mushroom4.png'))]
enemies.append([bottomLeft[0], bottomLeft[1]-140, images, 'Mushroom', 'most basic of enemies, can apply spores at intervals', MushroomShow, MushroomAttack, 17, 140, 140])
