import pygame
from random import randint
pygame.init()
cardWIDTH = 100
cardHEIGHT = 150


class Card:
    def __init__(self, x, y, screenX, screenY, used, image, name, description, ichorCost, exhaust, select):
        # integers between 0 and 4
        self.x = x
        self.y = y
        # a random id that should be unique
        self.id = randint(1, 1000000000000)
        # name of the card
        self.name = name
        # description of the card
        self.description = description
        # tells the cost of playing the card
        self.ichorCost = ichorCost
        # co-ordinates of the screen
        self.screenX = screenX
        self.screenY = screenY
        # co-ordinates of the screen including resolution
        self.resizedX = screenX
        self.resizedY = screenY
        # the definition used when the card is used
        self.used = used
        # the original image for the card and the size of the image
        self.image = image
        # creates these variables purely so my IDE doesn't get mad at me
        self.resizedImageSize = ()
        self.resizedImage = image
        # a variable that tells if the card will be removed from the deck after being used
        self.exhaust = exhaust
        self.select = select

    def draw(self, screen):
        # draws the resized image on screen
        screen.blit(self.resizedImage, (self.resizedX, self.resizedY))

    def resize(self, scaleWidth, scaleHeight):
        # resizes the image and location of image
        self.resizedX = int(self.screenX * scaleWidth) + 1
        self.resizedY = int(self.screenY * scaleHeight) + 1
        self.resizedImageSize = (int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1)
        self.resizedImage = pygame.transform.scale(self.image, self.resizedImageSize)

    def use(self, board, blankBoard, ichorLeft, enemy, scaleWidth, scaleHeight, turn):
        # checks whether the player has enough ichor to play the card
        if ichorLeft >= self.ichorCost:
            # subtracts ichorLeft by the ichor cost
            # plays the cards definition when used
            used, enemy, board = self.used(self, enemy=enemy, board=board, blankBoard=blankBoard, scaleWidth=scaleWidth, scaleHeight=scaleHeight, turn=turn)
            # returns different things depending on whether the card exausted, got played, or didn't
            if used:
                ichorLeft -= self.ichorCost
                if self.exhaust:
                    return 2, ichorLeft, enemy, board
                return 1, ichorLeft, enemy, board
        return 0, ichorLeft, enemy, board


class Enemy:
    def __init__(self, x, y, images, name, description, attackShow, attack, hp, width, height):
        # location of the image of the enemy and
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        # resized location of the image of the enemy
        self.resizedX = x
        self.resizedY = y
        self.resizedImageSize = (width, height)
        # images of the enemy
        self.images = images
        # resized images of the enemy
        self.resizedImages = images
        # name of the enemy
        self.name = name
        # the description of the enemy
        self.description = description
        # the enemy's attack
        self.attackShow = attackShow
        self.attack = attack
        # the enemy's hp
        self.hp = hp
        # effects that the enemy can have
        self.crippling = 0
        # symbols that will be drawn with the character in some circumstances
        self.symbols = []
        self.resizedSymbols = []
        self.resizedSymbolSize = (20, 20)

    def draw(self, screen, globalCounter):
        # draws the card
        screen.blit(self.resizedImages[int(globalCounter / 10) % len(self.resizedImages)], (self.resizedX, self.resizedY))
        counter = 0
        for symbol in self.resizedSymbols:
            screen.blit(symbol, (self.resizedX+int(counter*self.resizedSymbolSize[0]), int(self.resizedY + self.resizedImageSize[1] + self.resizedSymbolSize[1])))
            counter += 1.2

    def turn(self, turn, board):
        # reduces effects
        if self.crippling > 0:
            self.crippling -= 1
        # runs the attack definition
        board = self.attackShow(self, turn, board)
        return board

    def resize(self, scaleWidth, scaleHeight):
        # resizes the image and location of image
        self.resizedX = int(self.x * scaleWidth) + 1
        self.resizedY = int(self.y * scaleHeight) + 1
        self.resizedImageSize = (int(self.width * scaleWidth) + 1, int(self.height * scaleHeight) + 1)
        self.resizedImages = []
        self.resizedSymbols = []
        self.resizedSymbolSize = (int(20 * scaleWidth) + 1, int(20 * scaleHeight) + 1)
        for symbol in self.symbols:
            self.resizedSymbols.append(pygame.transform.scale(symbol, self.resizedSymbolSize))
        for image in self.images:
            self.resizedImages.append(pygame.transform.scale(image, self.resizedImageSize))

    def hit(self, damage):
        if self.crippling > 0:
            self.hp -= int(damage * 1.2)
        else:
            self.hp -= damage


class Mouse:
    def __init__(self):
        pass


class Button:
    def __init__(self, x, y, width, height, use, colour):
        self.x = x
        self.y = y
        self.resizedX = x
        self.resizedY = y
        self.width = width
        self.height = height
        self.resizedWidth = width
        self.resizedHeight = height
        self.use = use
        self.colour = colour

    def resize(self, scaleWidth, scaleHeight):
        self.resizedX = int(self.x * scaleWidth) + 1
        self.resizedY = int(self.y * scaleHeight) + 1
        self.resizedWidth = int(self.width * scaleWidth) + 1
        self.resizedHeight = int(self.height * scaleHeight) + 1

    def draw(self, screen):
        pygame.draw.rect(screen, self.colour, (self.resizedX, self.resizedY, self.resizedWidth, self.resizedHeight))
