import pygame, sys, random, math
from pygame.math import  Vector2

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
drawSurf = pygame.Surface((200,200))

clock = pygame.time.Clock()

flowers = {
    "sunflower":{"frames":21,"color":"yellow"},
    "rose":{"frames":13,"color":"red"}
}

flowerList = []
class Flower:
    def __init__(self, type):
        self.type = type
        self.height = 0 #Do not manually increment this var, may result in error being thrown. Use addHeight() instead.
        self.water = 0
        self.sunlight = 0
        self.frames = [pygame.image.load(f'Assets/{self.type}/{x}.png').convert_alpha() for x in range(flowers[self.type]["frames"])]
        flowerList.append(self)

    def Draw(self):
        drawSurf.blit(self.frames[self.height], (flowerList.index(self)*20,(-(self.frames[0].get_height()))+180))

    def addHeight(self, amount):
        self.height += amount
        if self.height > len(self.frames) - 1:
            self.height = len(self.frames) - 1

sunflower = Flower("sunflower")
rose = Flower("rose") 

sinVal = 0
sunlight = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    drawSurf.fill((255,255,255))
    for flower in flowerList:
        flower.Draw()

    sinVal += 0.01
    sunlight = (math.sin(sinVal)+1)*50

    screen.blit(pygame.transform.scale(drawSurf,(WIDTH,HEIGHT)),(0,0))
    pygame.display.update()
    clock.tick(60)