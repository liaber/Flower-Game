import pygame, sys, random, math
from pygame.math import  Vector2, clamp

pygame.init()

WIDTH, HEIGHT = 800, 800
screen = pygame.display.set_mode((WIDTH,HEIGHT))
drawSurf = pygame.Surface((200,200))

clock = pygame.time.Clock()

def pivotRot(img, angle, pivot, origin):
    surf = pygame.transform.rotate(img, -angle)
    offset = pivot + (origin - pivot).rotate(angle)
    rect = surf.get_rect(center=offset)
    return surf, rect


flowers = {
    "sunflower":{"frames":21,"color":"yellow"},
    "rose":{"frames":12,"color":"red"},
    "violet":{"frames":12,"color":"violet"}
}

flowerList = []
class Flower:
    def __init__(self, type):
        self.type = type
        self.height = 0 #Do not manually increment this var, may result in error being thrown. Use addHeight() instead.
        self.water = 50
        self.frames = [pygame.image.load(f'Assets/{self.type}/{x}.png').convert_alpha() for x in range(flowers[self.type]["frames"])]
        flowerList.append(self)

    def Draw(self):
        drawSurf.blit(self.frames[self.height], (flowerList.index(self)*20,(-(self.frames[0].get_height()))+180))

    def addHeight(self, amount):
        self.height += amount
        if self.height > len(self.frames) - 1:
            self.height = len(self.frames) - 1

class WaterCan:
    def __init__(self):
        self.rot = 0
        self.img = pygame.image.load("Assets/water-can.png").convert_alpha()

    def Draw(self):
        rotdCan = pivotRot(self.img, self.rot, Vector2((pygame.mouse.get_pos()[0]/4),(pygame.mouse.get_pos()[1]/4)), Vector2((pygame.mouse.get_pos()[0]/4)-7,(pygame.mouse.get_pos()[1]/4)+11))
        drawSurf.blit(rotdCan[0],rotdCan[1])

sunflower = Flower("sunflower")
rose = Flower("rose") 
violet = Flower("violet")

waterCan = WaterCan()

sinVal = 0
sunlight = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            waterCan.rot+=45
        if event.type == pygame.MOUSEMOTION:
            print(type(event.rel))

    drawSurf.fill((255,255,255))
    for flower in flowerList:
        flower.Draw()
        flower.water = clamp(flower.water-(sunlight/50000),0,100)
        if random.randint(1,100) == 1:
            flower.addHeight(1)

    sinVal += 1
    sunlight = (math.sin(sinVal/1000)+1)*100

    waterCan.Draw()

    screen.blit(pygame.transform.scale(drawSurf,(800,800)),(0,0))
    pygame.display.flip()
    clock.tick(60)