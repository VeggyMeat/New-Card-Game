import pygame
pygame.init()


class card:
    def __init__(self, x, y, screenX, screenY, used, image, imageSize, scaleWidth, scaleHeight):
        # integers between 0 and 4
        self.x = x
        self.y = y
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

    def draw(self, screen, scaleWidth, scaleHeight):
        screen.blit(self.resizedImage, (self.resizedX, self.resizedY))

    def resize(self, scaleWidth, scaleHeight):
        self.resizedX = int(self.screenX * scaleWidth)
        self.resizedY = int(self.screenY * scaleHeight)
        self.resizedImageSize = (int(self.imageSize[0] * scaleWidth), int(self.imageSize[1] * scaleHeight))
        self.resizedImage = pygame.transform.scale(self.image, self.resizedImage)
