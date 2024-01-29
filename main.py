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

def rotPoint(p1:Vector2, p2:Vector2, angle:int):
    angle = (angle*math.pi)/180
    return Vector2((((p1.x-p2.x)*math.cos(angle))-((p1.y-p2.y)*math.sin(angle)))+p2.x,((p1.x-p2.x)*math.sin(angle))+((p1.y-p2.y)*math.cos(angle))+p2.y)

class PolarCord:
    def __init__(self, rad, angle):
        self.rad = rad
        self.angle = angle

    def get_cartesian(self):
        return (math.cos(self.angle)*self.rad,math.sin(self.angle)*self.rad)

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
        self.potRect = pygame.Rect(flowerList.index(self)*20,(-(self.frames[0].get_height()))+140+self.frames[0].get_height()-20,20,20)

    def Draw(self):
        drawSurf.blit(self.frames[self.height], (flowerList.index(self)*20,(-(self.frames[0].get_height()))+140))
        pygame.draw.rect(drawSurf, (255,255,255), pygame.Rect((flowerList.index(self)*20)+8,((-(self.frames[0].get_height()))+140)+self.frames[0].get_height()+5,4,40),border_radius=2)
        percent = int(round((clamp(self.water,0,100)/100)*40,0))
        pygame.draw.rect(drawSurf, (99,155,255), pygame.Rect((flowerList.index(self)*20)+8,((-(self.frames[0].get_height()))+140)+self.frames[0].get_height()+5+(40-percent),4,percent),border_radius=2)
        drawSurf.blit(pygame.image.load("Assets/water.png").convert_alpha(),Vector2((flowerList.index(self)*20)+8,((-(self.frames[0].get_height()))+140)+self.frames[0].get_height()+48))

    def addHeight(self, amount):
        self.height += amount
        if self.height > len(self.frames) - 1:
            self.height = len(self.frames) - 1

class WaterCan:
    def __init__(self, rot=0):
        self.rot = rot
        self.img = pygame.image.load("Assets/water-can.png").convert_alpha()
        self.selected = False

    def Draw(self):
        if self.selected == True:
            rotdCan = pivotRot(self.img, self.rot, Vector2((pygame.mouse.get_pos()[0]/4),(pygame.mouse.get_pos()[1]/4)), Vector2((pygame.mouse.get_pos()[0]/4)-7,(pygame.mouse.get_pos()[1]/4)+11))
            drawSurf.blit(rotdCan[0],rotdCan[1])
        if self.selected == False:
            drawSurf.blit(self.img,Vector2((WIDTH/4)-5-self.img.get_width(),5))

    def Update(self, rel):
        print(rel)
        if rel[0] != 0:
            rel = Vector2(-rel[0],-rel[1])
            self.rot += math.atan(rel.y/rel.x)*(180/math.pi)

water = []
class WaterParticle:
    def __init__(self, pos:Vector2, velo=Vector2()):
        self.pos = pos
        self.velo = velo
        water.append(self)

    def Draw(self):
        '''drawSurf.set_at((int(self.pos.x),int(self.pos.y)), (99,155,255))
        if not (self.velo.x == 0 and self.velo.y == 0):
            newVec = self.pos-self.velo.normalize()
            drawSurf.set_at((int(newVec.x),int(newVec.y)), (99,155,255))
            newVec -= self.velo.normalize()
            drawSurf.set_at((int(newVec.x),int(newVec.y)), (99,155,255))'''
        pygame.draw.line(drawSurf,(99,155,255),self.pos,self.pos-self.velo)

    def Update(self):
        collide = False
        self.velo.y += 0.5
        self.pos.y += self.velo.y
        for flower in flowerList:
            if flower.potRect.collidepoint(self.pos):
                flower.water += 1
                collide = True

        self.velo.x *= 0.95
        self.pos.x += self.velo.x
        for flower in flowerList:
            if flower.potRect.collidepoint(self.pos):
                flower.water += 0.5
                collide = True
        
        if collide == True:
            water.remove(self)

sunflower = Flower("sunflower")
rose = Flower("rose") 
violet = Flower("violet")

waterCan = WaterCan(rot=0)

sinVal = 0
sunlight = 0

mpos = Vector2(0,0)

while True:
    prevmpos = mpos
    mpos = Vector2(pygame.mouse.get_pos()[0]/4,pygame.mouse.get_pos()[1]/4)
    deltamouse = mpos-prevmpos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            waterCan.rot += 5
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                if waterCan.selected == False:
                    if pygame.Rect((WIDTH/4)-5-waterCan.img.get_width(),5,waterCan.img.get_width(),waterCan.img.get_height()).collidepoint(mpos):
                        waterCan.selected = not waterCan.selected
                        waterCan.img = pygame.image.load("Assets/water-can.png").convert_alpha()
                else:
                    for i in range(10):
                        WaterParticle(rotPoint(mpos+Vector2(-19,11),mpos,waterCan.rot),velo=Vector2(random.randint(-5,-1),random.randint(-5,-1)))
            if event.button == 3:
                if waterCan.selected == True:
                    waterCan.selected = not waterCan.selected
                    waterCan.rot = 0
    
    if waterCan.selected == False:
        if pygame.Rect((WIDTH/4)-5-waterCan.img.get_width(),5,waterCan.img.get_width(),waterCan.img.get_height()).collidepoint(mpos):
            waterCan.img = pygame.image.load("Assets/water-can-highlight.png").convert_alpha()
        else:
            waterCan.img = pygame.image.load("Assets/water-can.png").convert_alpha()

    drawSurf.fill((0,0,0))
    for flower in flowerList:
        flower.Draw()
        flower.water = clamp(flower.water-(sunlight/5000),0,100)
        if random.randint(1,1000) == 1:
            if flower.water >= 70:
                flower.addHeight(1)

    sinVal += 1
    sunlight = (math.sin(sinVal/1000)+1)*100

    waterCan.Draw()
    #waterCan.Update(deltamouse)
    for drop in water:
        drop.Update()
        drop.Draw()
    #pygame.draw.circle(drawSurf,(255,0,0),rotPoint(mpos+Vector2(-19,11),mpos,waterCan.rot),1)
    screen.blit(pygame.transform.scale(drawSurf,(800,800)),(0,0))

    pygame.display.flip()
    clock.tick(60)