from random import randint
from copy import deepcopy
import pygame
from Classes import Enemy
from pathlib import Path
enemies = []
# base for adding in the dictionaries for the cards and the root of where the images are
blankCard = {'images': False, 'name': False, 'description': False, 'attack': False, 'hp': False, 'width': False, 'height': False}
enemyRoot = Path('Images/Enemies/')
bottomLeft = (900, 900)

# enemies


def MushroomShow(turn, board, hp):
    board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    number = randint(1, 4)
    if number == 1:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
    if number <= 2:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['spores'] += 1
    if turn % 3 == 1:
        for row in board:
            for card in row:
                hp -= card['spores']
    return hp, board


def MushroomAttack(turn, board, hp):
    if turn % 3 == 1:
        for row in board:
            for card in row:
                hp -= card['spores']
                card['spores'] = 0
    return hp, board


images = [pygame.image.load(enemyRoot/'Mushroom1.png'), pygame.image.load(enemyRoot/'Mushroom2.png'), pygame.image.load(enemyRoot/'Mushroom3.png'), pygame.image.load(enemyRoot/'Mushroom4.png')]
enemies.append(Enemy(bottomLeft[0], bottomLeft[1]-140, images, 'Mushroom', 'most basic of enemies, can apply spores at intervals', MushroomShow, MushroomAttack, 17, 140, 140))
