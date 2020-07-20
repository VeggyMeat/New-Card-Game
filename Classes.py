import pygame
pygame.init()
cards = []


class card:
    def __init__(self, x, y, screenX, screenY, used, image, imageSize, scaleWidth, scaleHeight, name, description, ichorCost, exhaust=False):
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
        self.imageSize = imageSize
        # creates these variables purely so my IDE doesn't get mad at me
        self.resizedImageSize = ()
        self.resizedImage = image
        # resizes the image to the players monitor screen (hopefully)
        self.resize(scaleWidth, scaleHeight)
        # a variable that tells if the card will be removed from the deck after being used
        self.exhaust = exhaust

    def draw(self, screen):
        screen.blit(self.resizedImage, (self.resizedX, self.resizedY))

    def resize(self, scaleWidth, scaleHeight):
        self.resizedX = int(self.screenX * scaleWidth)
        self.resizedY = int(self.screenY * scaleHeight)
        self.resizedImageSize = (int(self.imageSize[0] * scaleWidth), int(self.imageSize[1] * scaleHeight))
        self.resizedImage = pygame.transform.scale(self.image, self.resizedImage)

    def use(self):
        self.used()
        if self.exhaust:
            return True
        return False
