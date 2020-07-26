import pygame
from random import randint
pygame.init()
cardWIDTH = 100
cardHEIGHT = 150


class Card:
    def __init__(self, x, y, screenX, screenY, used, image, name, description, ichorCost, exhaust):
        # integers between 0 and 4
        self.x = x
        self.y = y
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

    def draw(self, screen):
        # draws the resized image on screen
        screen.blit(self.resizedImage, (self.resizedX, self.resizedY))

    def resize(self, scaleWidth, scaleHeight):
        # resizes the image and location of image
        self.resizedX = int(self.screenX * scaleWidth) + 1
        self.resizedY = int(self.screenY * scaleHeight) + 1
        self.resizedImageSize = (int(cardWIDTH * scaleWidth) + 1, int(cardHEIGHT * scaleHeight) + 1)
        self.resizedImage = pygame.transform.scale(self.image, self.resizedImageSize)

    def use(self, board, blankBoard, ichorLeft, enemy):
        # checks whether the player has enough ichor to play the card
        if ichorLeft >= self.ichorCost:
            # subtracts ichorLeft by the ichor cost
            ichorLeft -= self.ichorCost
            # plays the cards definition when used
            self.used(enemy=enemy, board=board, blankBoard=blankBoard)
            # returns different things depending on whether the card exausted, got played, or didn't
            if self.exhaust:
                return 2, ichorLeft
            return 1, ichorLeft
        return 0, ichorLeft


class Enemy:
    def __init__(self, x, y, images, name, description, attack, hp, width, height):
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
        self.attack = attack
        # the enemy's hp
        self.hp = hp
        # effects that the enemy can have
        self.crippling = 0
        # resizing character sprites

    def draw(self, screen, globalCounter):
        # draws the card
        screen.blit(self.resizedImages[int(globalCounter / 10) % len(self.resizedImages)], (self.resizedX, self.resizedY))

    def turn(self, turn, board, hp):
        # reduces effects
        if self.crippling > 0:
            self.crippling -= 1
        # runs the attack definition
        self.attack(turn, board, hp)

    def resize(self, scaleWidth, scaleHeight):
        # resizes the image and location of image
        self.resizedX = int(self.x * scaleWidth) + 1
        self.resizedY = int(self.y * scaleHeight) + 1
        self.resizedImageSize = (int(self.width * scaleWidth) + 1, int(self.height * scaleHeight) + 1)
        self.resizedImages = []
        for image in self.images:
            self.resizedImages.append(pygame.transform.scale(image, self.resizedImageSize))


class Mouse:
    def __init__(self):
        pass
