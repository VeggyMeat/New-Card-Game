from random import randint
from copy import deepcopy
import pygame
from Definitions import shuffle
from pathlib import Path
from Classes import Card
# sets up some variables
cards = []
cardRoot = Path("Images/Cards/")

# cards


def LuckOfTheDice(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # sets up some variables
        newBoard = deepcopy(blankBoard)
        counter1 = 0

        # makes a order which goes from (0,0) to (4,4)
        order = []

        for x in range(5):
            for y in range(5):
                order.append((x, y))
        # copies this order and shuffles it into different sections
        blankOrder = {'card': shuffle(deepcopy(order)), 'playable': shuffle(deepcopy(order)), 'attacked': shuffle(deepcopy(order)), 'spores': shuffle(deepcopy(order)), 'block': shuffle(deepcopy(order))}

        # loops through all cards
        for row in board:
            counter2 = 0
            for card in row:
                # loops through each type of the card
                for type in card:
                    # finds new places for the card's type to go based on the order for its type
                    cordsX = blankOrder[type][counter1*5+counter2][0]
                    cordsY = blankOrder[type][counter1*5+counter2][1]

                    # moves it to these ne places
                    newBoard[cordsX][cordsY][type] = card[type]

                    # checks if the type is the card class and if so resizes and adds the new co-ordinates for the card
                    if type == 'card' and newBoard[cordsX][cordsY][type] != False:
                        newBoard[cordsX][cordsY][type].x, newBoard[cordsX][cordsY][type].y, newBoard[cordsX][cordsY][type].screenX, newBoard[cordsX][cordsY][type].screenY = cordsX, cordsY, 120 * cordsX + 50, 170 * cordsY + 50
                        newBoard[cordsX][cordsY][type].resize(scaleWidth=scaleWidth, scaleHeight=scaleHeight)
                counter2 += 1
            counter1 += 1
        # returns saying that it was played
        return True, enemy, newBoard
    # returns saying it wasn't able to be played
    return False, enemy, board


# appends this newly made card not in a class format so many can be made many times
cards.append([LuckOfTheDice, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'luck of the dice', 'usable once a combat which randomly moves all cards, playable positions and where the enemies will attack, for no ichor', 0, False, False])


def StrikeAtTheHeart(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    # checks if the card is on a playable tile
    if board[self.x][self.y]['playable']:
        # applies its effects to the enemy
        enemy.crippling += 2
        enemy.hit(15)

        # returns sating that it was played
        return True, enemy, board
    # returns saying that it wasn't able to be played
    return False, enemy, board


# appends this newly made card not in a class format so many can be made many times
cards.append([StrikeAtTheHeart, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'strike at the heart', 'high cost, medium damage, status effect, single target', 3, False, True])


def SneakAttack(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    # checks if the card is on a playable tile or if its turn 1
    if board[self.x][self.y]['playable'] or turn == 1:
        # applies damage to the enemy
        enemy.hit(5)

        # returns sating that it was played
        return True, enemy, board
    # returns saying that it wasn't able to be played
    return False, enemy, board


# appends this newly made card not in a class format so many can be made many times
cards.append([SneakAttack, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'sneak attack', 'low cost, low damage, single target', 1, False, True])


def Execute(self, enemy, board, blankBoard, scaleWidth, scaleHeight, turn):
    # checks if the card is on a playable tile or the enemy is able to be one shot by the card
    if board[self.x][self.y]['playable'] or enemy.hp <= 10:
        # applies damage to the enemy
        enemy.hit(10)

        # returns sating that it was played
        return True, enemy, board
    # returns saying that it wasn't able to be played
    return False, enemy, board


# appends this newly made card not in a class format so many can be made many times
cards.append([Execute, pygame.image.load(str(cardRoot / 'StrikeAtTheHeart.png')), 'execute', 'medium cost with medium damage, single target', 2, False, True])
