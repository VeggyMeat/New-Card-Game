from random import randint
from copy import deepcopy
import pygame
from Definitions import shuffle
from pathlib import Path
from Classes import Card
cards = []
# base for adding in the dictionaries for the cards and the root of where the images are
blankCard = {'used': False, 'image': False, 'name': False, 'description': False, 'ichorCost': False, 'exhaust': False}
cardRoot = Path("Images/Cards/")

# cards


def LuckOfTheDice(enemy, board, blankBoard, scaleWidth, scaleHeight):
    newBoard = deepcopy(blankBoard)
    counter1 = 0
    order = []
    for x in range(5):
        for y in range(5):
            order.append((x, y))
    blankOrder = {'card': shuffle(deepcopy(order)) , 'playable': shuffle(deepcopy(order)), 'attacked': shuffle(deepcopy(order)), 'spores': shuffle(deepcopy(order)), 'block': shuffle(deepcopy(order))}
    for row in board:
        counter2 = 0
        for card in row:
            for type in card:
                cordsX = blankOrder[type][counter1*5+counter2][0]
                cordsY = blankOrder[type][counter1*5+counter2][1]
                newBoard[cordsX][cordsY][type] = card[type]
                if type == 'card' and newBoard[cordsX][cordsY][type] != False:
                    newBoard[cordsX][cordsY][type].x, newBoard[cordsX][cordsY][type].y, newBoard[cordsX][cordsY][type].screenX, newBoard[cordsX][cordsY][type].screenY = cordsX + 1, cordsY + 1, 120 * cordsX + 50, 170 * cordsY + 50
                    newBoard[cordsX][cordsY][type].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
            counter2 += 1
        counter1 += 1
    print("done")
    return enemy, newBoard


cards.append([LuckOfTheDice, pygame.image.load(cardRoot / 'StrikeAtTheHeart.png'), 'luck of the dice', 'usable once a combat which randomly moves all cards, playable positions and where the enemies will attack, for no ichor', 0, True])


def StrikeAtTheHeart(enemy, board, blankBoard, scaleWidth, scaleHeight):
    enemy.crippling += 2
    enemy.hp -= 15
    return enemy, board


cards.append([StrikeAtTheHeart, pygame.image.load(cardRoot / 'StrikeAtTheHeart.png'), 'strike at the heart', 'high cost, medium damage, status effect, single target', 3, False])
