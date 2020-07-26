from random import randint
from copy import deepcopy
from pathlib import Path
import pygame
from Classes import Card
cards = []
# base for adding in the dictionaries for the cards and the root of where the images are
blankCard = {'used': False, 'image': False, 'name': False, 'description': False, 'ichorCost': False, 'exhaust': False}

# use pathlib to set file source directory, NORMAL SLASHES
cardRoot = Path("Images/Cards/")

# cards


def LuckOfTheDice(enemy, board, blankBoard):
    newBoard = deepcopy(blankBoard)
    for row in board:
        for card in row:
            for type in card:
                while not card[type]:
                    cords = (randint(1, 5), randint(1, 5))
                    if not newBoard[cords[0]][cords[1]][type]:
                        newBoard[cords[0]][cords[1]][type] = card[type]
                        card[type] = False
    return newBoard


cards.append(Card(False, False, False, False, LuckOfTheDice, False, 'luck of the dice', 'usable once a combat which randomly moves all cards, playable positions and where the enemies will attack, for no ichor', 0, True))


def StrikeAtTheHeart(enemy, board, blankBoard):
    enemy.crippling += 2
    enemy.hp -= 15


cards.append([False, False, False, False, StrikeAtTheHeart, pygame.image.load(str(cardRoot/'StrikeAtTheHeart.png')), 'strike at the heart', 'high cost, medium damage, status effect, single target', 3, False])
