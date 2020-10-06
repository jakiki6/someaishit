#!/usr/bin/python3

from ai import ai_magic

import pygame, time, datetime, os, random, json, base64, threading

pygame.mixer.quit()

if os.path.isfile("conf.json"):
    conffile = open("conf.json", "r")
    conf = json.loads("\n".join(conffile.readlines()))
    conffile.close()
else:
    json.dump({"base" : 16, "fps" : 60, "font" : ["Roboto", 30], "height" : 512, "width" : 512, "counter": {"snake" : 12, "power" : 600}}, indent=4, fp=open("conf.json", "w"))
    exit(0)
#conf
base = int(conf["base"])
fps = int(conf["fps"])
fontname = conf["font"] [0]
fontsize = int(conf["font"][1])
h = int(conf["height"])
w = int(conf["width"])
snakec = int(conf["counter"] ["snake"])
powerc = int(conf["counter"] ["power"])
#endconf
pygame.init()
pygame.font.init()
snakeGroup = pygame.sprite.Group()
powerupGroup = pygame.sprite.Group()
isrunning = True
size = h, w
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Snakefight")
font = pygame.font.SysFont(fontname, fontsize)
uhr = pygame.time.Clock()
def init():
    snakeGroup.add(Snake("1.png", 0, 5, {119 : [0, -1], 115 : [0, 1], 97 : [-1, 0], 100 : [1, 0]}, "Snake 1", [0, 1], False, 5)) # Img, startxtile, startytile, keys(Key-ID : move), name, startdirection, lenght
    sn = Snake("2.png", 31, 26, {273 : [0, -1], 274 : [0, 1], 276 : [-1, 0], 275 : [1, 0]}, "Snake 2", [0, -1], True, 5)
    snakeGroup.add(sn)
    threading.Thread(target=ai_magic, args=(sn,), daemon = True).start()
    isrunning = True
class Snake(pygame.sprite.Sprite):
    def __init__(self, img, x, y, keys, name, direction, ai, startlen = 3):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * base + startlen, y * base)
        self.keys = keys
        self.name = name
        self.list = []
        #self.list.append([x, y])
        self.move = direction
        self.powerp = 0
        offsetx, offsety = direction
        for n in range(0, startlen):
            self.list.append([x - offsetx, y - offsety])
        self.ai = ai
    def draw(self):
        for pos in self.list:
            screen.blit(self.image, (pos[0] * base, pos[1] * base))
    def keydown(self, key):
        if not key in self.keys.keys(): return
        self.move = self.keys[key]
    def loose(self):
        #return #Cheat
        n = 0
        for sn in snakeGroup.sprites():
            n += 1
        if n == 2:
            isrunning = False
            for snake in snakeGroup.sprites():
                if snake.name != self.name:
                    if snake.list[0] in self.list:
                        snake.name = "Nobody"
                    screen.fill((255, 100, 0))
                    rendered_text = font.render(snake.name + " won!", True, (0, 0, 0))
                    screen.blit(rendered_text, (h / 2 - rendered_text.get_height() / 2, w / 2 - rendered_text.get_width() / 2))
                    pygame.display.flip()
                    time.sleep(3)
                    for sn in snakeGroup.sprites():
                        if snake.name != self.name: sn.kill()
                    for pu in powerupGroup.sprites(): pu.kill()
                    self.kill()
                    init()
        else:
            self.kill()
    def update(self):
        newpos = self.list[0].copy()
        newpos[0] += self.move[0]
        newpos[1] += self.move[1]
        self.list = [newpos,] + self.list
        if self.powerp == 0:
            del(self.list[len(self.list) - 1])
        else:
            self.powerp -= 1
        self.draw()
        if not isrunning:
            return
        pos = self.list[0]
        if pos[0] > w // base:
            pos[0] = 0
        elif pos[1] > h // base:
            pos[1] = 0
        elif pos[0] < 0:
            pos[0] = w // base
        elif pos[1] < 0:
            pos[1] = h // base
        if pos in self.list[1:]:
            self.loose()
        for snake in snakeGroup.sprites():
            if pos in snake.list and snake.name != self.name:
                self.loose()
        for pu in powerupGroup.sprites():
            if pos == pu.pos:
                self.powerp += 1
                pu.kill()
class Powerup(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("Powerup.png")
        self.rect = self.image.get_rect()
        self.rect.topleft = (x * base, y * base)
        self.pos = [x, y]

init()
tickc = 0
while True:
    screen.fill((255, 255, 255))
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            for snake in snakeGroup.sprites():
                snake.keydown(event.key)
            if event.key == pygame.K_F12:
                pygame.image.save(screen, str(datetime.datetime.now()) + ".png")
                screen.fill((0, 0, 0))
                pygame.display.flip()
                time.sleep(0.2)
                screen.fill((255, 255, 255))
        elif event.type == pygame.QUIT:
            quit()
    uhr.tick(fps)
    if tickc % snakec == 0:
        snakeGroup.update()
        powerupGroup.draw(screen)
        pygame.display.flip()
    if tickc % powerc == 0:
        powerupGroup.add(Powerup(random.randint(0, h / base), random.randint(0, w / base)))
    tickc += 1
        
