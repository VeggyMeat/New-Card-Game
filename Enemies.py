from random import randint
from copy import deepcopy
from pathlib import Path
import pygame
from Classes import Enemy
enemies = []
# base for adding in the dictionaries for the cards and the root of where the images are
blankCard = {'images': False, 'name': False, 'description': False, 'attack': False, 'hp': False, 'width': False, 'height': False}
cardRoot = Path('Images/Enemies/')
bottomLeft = (900, 900)

# enemies


def Mushroom(turn, board, hp):
    board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    number = randint(1, 4)
    if number == 1:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['effects']['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['effects']['spores'] += 1
    if number <= 2:
        board[randint(0, 4)][randint(0, 4)]['attacked'] += 1
    else:
        board[randint(0, 4)][randint(0, 4)]['effects']['spores'] += 1
        board[randint(0, 4)][randint(0, 4)]['effects']['spores'] += 1
    if turn % 3 == 1:
        for row in board:
            for card in row:
                hp -= card['effects']['spores']
    return hp


images = [pygame.image.load(str(cardRoot / 'Mushroom1.png')), pygame.image.load(str(cardRoot / 'Mushroom2.png')), pygame.image.load(str(cardRoot / 'Mushroom3.png')), pygame.image.load(str(cardRoot / 'Mushroom4.png'))]
enemies.append(Enemy(bottomLeft[0], bottomLeft[1]-35, images, 'Mushroom', 'most basic of enemies, can apply spores at intervals', Mushroom, 17, 35, 35))
