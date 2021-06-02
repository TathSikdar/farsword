import pygame

class StaticImage():
    def __init__(self, surface, image):
        self.image = pygame.image.load(image)
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.rect = self.image.get_rect()
        self.surface = surface

    def scale(self, resolutionTuple):
        self.image = pygame.transform.scale(self.image, resolutionTuple)
        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def display(self, x, y):
        self.rect.x = x
        self.rect.y = y
        self.surface.blit(self.image, (self.rect.x,self.rect.y))