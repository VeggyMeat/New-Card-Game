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


def LuckOfTheDice(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    if board[self.x][self.y]['playable']:
        newBoard = deepcopy(blankBoard)
        counter1 = 0
        order = []
        for x in range(5):
            for y in range(5):
                order.append((x, y))
        blankOrder = {'card': shuffle(deepcopy(order)), 'playable': shuffle(deepcopy(order)), 'attacked': shuffle(deepcopy(order)), 'spores': shuffle(deepcopy(order)), 'block': shuffle(deepcopy(order))}
        for row in board:
            counter2 = 0
            for card in row:
                for type in card:
                    cordsX = blankOrder[type][counter1*5+counter2][0]
                    cordsY = blankOrder[type][counter1*5+counter2][1]
                    newBoard[cordsX][cordsY][type] = card[type]
                    if type == 'card' and newBoard[cordsX][cordsY][type] != False:
                        newBoard[cordsX][cordsY][type].x, newBoard[cordsX][cordsY][type].y, newBoard[cordsX][cordsY][type].screenX, newBoard[cordsX][cordsY][type].screenY = cordsX, cordsY, 120 * cordsX + 50, 170 * cordsY + 50
                        newBoard[cordsX][cordsY][type].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
                counter2 += 1
            counter1 += 1
        return True, enemy, newBoard
    return False, enemy, board


cards.append([LuckOfTheDice, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'luck of the dice', 'usable once a combat which randomly moves all cards, playable positions and where the enemies will attack, for no ichor', 0, False])


def StrikeAtTheHeart(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    if board[self.x][self.y]['playable']:
        enemy.crippling += 2
        enemy.hp -= 15
        return True, enemy, board
    return False, enemy, board


cards.append([StrikeAtTheHeart, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'strike at the heart', 'high cost, medium damage, status effect, single target', 3, False])


def SneakAttack(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    if board[self.x][self.y]['playable'] or turn == 1:
        enemy.hp -= 5


cards.append([SneakAttack, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'sneak attack', 'low cost, low damage, single target', 1, False])


def Execute(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    if board[self.x][self.y]['playable'] or enemy.hp <= 10:
        enemy.hp -= 10


cards.append([Execute, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'execute', 'medium cost with medium damage, single target', 2, False])
