from random import randint
from copy import deepcopy
import pygame
cards = []
# base for adding in the dictionaries for the cards and the root of where the images are
blankCard = {'used': False, 'image': False, 'name': False, 'description': False, 'ichorCost': False, 'exhaust': False}
cardRoot = 'Images\\Cards\\'

# cards


def LuckOfTheDice(board, blankBoard):
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


cards.append({'used': LuckOfTheDice, 'image': False, 'name': 'luck of the dice', 'description': 'usable once a combat which randomly moves all cards, playable positions and where the enemies will attack for no ichor', 'ichorCost': 0, 'exhaust': True})


def StrikeAtTheHeart(enemy, board, blankBoard):
    enemy.crippling += 2
    enemy.hp -= 15


cards.append({'used': StrikeAtTheHeart, 'image': pygame.image.load(cardRoot+'StrikeAtTheHeart'), 'name': 'strike at the heart', 'description': 'high cost, medium damage, status effect, single target', 'ichorCost': 3, 'exhaust': False})
