import pygame
from random import randint
pygame.init()
cardWIDTH = 100
cardHEIGHT = 150
enemyX = 0
enemyY = 0


class Card:
    def __init__(self, x, y, screenX, screenY, used, image, scaleWidth, scaleHeight, name, description, ichorCost, exhaust):
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
        # resizes the image to the players monitor screen (hopefully)
        self.resize(scaleWidth, scaleHeight)
        # a variable that tells if the card will be removed from the deck after being used
        self.exhaust = exhaust

    def draw(self, screen):
        # draws the resized image on screen
        screen.blit(self.resizedImage, (self.resizedX, self.resizedY))

    def resize(self, scaleWidth, scaleHeight):
        # resizes the image and location of image
        self.resizedX = int(self.screenX * scaleWidth)
        self.resizedY = int(self.screenY * scaleHeight)
        self.resizedImageSize = (int(cardWIDTH * scaleWidth), int(cardHEIGHT * scaleHeight))
        self.resizedImage = pygame.transform.scale(self.image, self.resizedImage)

    def use(self, board, blankBoard, ichorLeft):
        # checks whether the player has enough ichor to play the card
        if ichorLeft >= self.ichorCost:
            # subtracts ichorLeft by the ichor cost
            ichorLeft -= self.ichorCost
            # plays the cards definition when used
            self.used(board=board, blankBoard=blankBoard)
            # returns different things depending on whether the card exausted, got played, or didn't
            if self.exhaust:
                return 2, ichorLeft
            return 1, ichorLeft
        return 0, ichorLeft


class Enemy:
    def __init__(self, x, y, image, name, description, attacks, attackOdds, hp):
        # location of the image of the card
        self.x = x
        self.y = y
        # image of the card
        self.image = image
        # name of the card
        self.name = name
        # the description of a card
        self.description = description
        # all the cards attacks and the odds of those happening
        self.attacks = attacks
        self.attackOdds = attackOdds
        # the enemies hp
        self.hp = hp
        # effects that the enemy can have
        self.crippling = 0

    def draw(self, screen):
        # draws the card
        screen.blit(self.image, enemyX, enemyY)

    def turn(self):
        # reduces effects
        if self.crippling > 0:
            self.crippling -= 1
        # randomly choses and acts out an attack
        number = randint(1, sum(self.attackOdds))
        total = 0
        counter = 0
        for odd in self.attackOdds:
            if odd <= number:
                self.attacks[counter]()
                break
            total += odd
            counter += 1
