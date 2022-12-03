from random import randint
from time import time as timer
from pygame import *

mixer.init()
mixer.music.load("main.ogg")
mixer.music.play()
drink_sound = mixer.Sound('drink_sound.ogg')
semki_sound = mixer.Sound('eat_sound.ogg')
lost_sound = mixer.Sound('lost_sound.ogg')

platofrm = "platform.png"
img_back = "atb.jfif"
img_hero = "gopnik.png"
img_hero_mirror = "gopnik_2.png"
img_enemy = "stone.png"
img_pivo = "pivo.png"
img_platform = "platform.png"
img_semki = "semki.png"
width, height = 700, 500
mw = display.set_mode((width, height))
display.set_caption("Gopnik jump")
background = transform.scale(image.load(img_back), (width, height))
lost = 0


font.init()
text = font.Font(None, 36)
text1 = font.Font(None, 80)
win = text1.render("Розкумар успешен!", True, (0, 255, 0))
lose = text1.render("Розкумар провален :(", True, (255, 0, 0))




class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, speed):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(
            image.load(player_image), (size_x, size_y))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
        self.size_x = size_x
        self.size_y = size_y 
    def reset(self):
        mw.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
            self.image = transform.scale(
            image.load("gopnik_2.png"), (self.size_x, self.size_y))
        if keys[K_RIGHT] and self.rect.x < width - 80:
            self.rect.x += self.speed
            self.image = transform.scale(
            image.load("gopnik.png"), (self.size_x, self.size_y))
        if keys[K_SPACE]:
            self.rect.y -= 8
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width-160)
            self.rect.y = 0
            lost += 1
            lost_sound.play()
'''   def reset(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            mw.blit("gopnik_2.png", (self.rect.x, self.rect.y)) 
        if keys[K_RIGHT] and self.rect.x < width - 80:
            mw.blit("gopnik.png", (self.rect.x, self.rect.y)) '''
            


class Pivo(GameSprite):
    def update(self):
        global lost
        self.rect.y += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width-160)
            self.rect.y = 0
            lost_sound.play()
class Platform(GameSprite):
    def update(self):
        global lost
        self.rect.x += self.speed
        if self.rect.y > height:
            self.rect.x = randint(80, width-160)
            self.rect.y = 0
            lost += 1
            lost_sound.play()

        

gopnik = Player(img_hero, 300, height - 100, 80, 100, 2)
stone = sprite.Group()
run = True
finish = False
score = 0
goal = 10
rel_time = False


stonegroup = sprite.Group()
semkigroup = sprite.Group()
pivogroup = sprite.Group()
for i in range(0, 3):
    pivo = Pivo(img_pivo, randint(80, 650),0, 40, 100, 1)
    pivogroup.add(pivo)
for i in range(0, 3):
    semki = Pivo(img_semki, randint(10, 650) ,0, 80, 100, 1)
    semkigroup.add(semki)
for i in range(0, 3):
    stone = Pivo(img_enemy, randint(0, 650), -40, 80, 100, randint(1, 3))
    stonegroup.add(stone)



while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
    if not finish:
        mw.blit(background, (0, 0))

        text_score = text.render("Счет: " + str(score), 1, (255, 255, 255))
        mw.blit(text_score, (10, 20))
        text_lost = text.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        mw.blit(text_lost, (10, 50))

        gopnik.update()
        gopnik.reset()
        
                                     
        stonegroup.draw(mw)

        pivogroup.draw(mw)

        semkigroup.draw(mw)
        for semki in semkigroup:
            semki.update()
        for stone in stonegroup:
            stone.update()
        for pivo in pivogroup:
            pivo.update()
        if sprite.spritecollide(gopnik, pivogroup,
                                    True):  
            score += 1
            pivo = Pivo(img_pivo, randint(80, 650),0, 40, 100, 1)
            pivogroup.add(pivo)
        if sprite.spritecollide(gopnik, semkigroup, True):
            score +=1
            semki = Pivo(img_semki, randint(10, 650) ,0, 80, 100, 1)
            semkigroup.add(semki)
            

    if sprite.spritecollide(gopnik, stonegroup, False) or lost >= 1:
        finish = True
        mw.blit(lose, (100, 200))

    if score >= goal:
        finish = True
        mw.blit(win,(100, 200))

    display.update()
    time.delay(50)
