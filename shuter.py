from pygame import *
from os import path
from random import randint



font.init()
mixer.init()
font = font.Font(None, 36)


img_back = 'galaxy.png'
img_blast = 'blust.png'
img_bullet = 'bullet.png'
img_enemy = 'enemy2.png'

score = 0
lost = 0

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, player_speed):
        sprite.Sprite.__init__(self)


        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y


    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))



class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x < win_width - 80:
            self.rect.x += self.speed

    def fire(self):
        bullet = Bullet(img_bullet, self.rect.right-20, self.rect.top, 15, 20, 15)
        bullet2 = Bullet(img_bullet, self.rect.left+5, self.rect.top, 15, 20, 15)
        bullet3 = Bullet(img_bullet, self.rect.centerx-8, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
        bullets.add(bullet2)
        bullets.add(bullet3)
    
    def fire_bluster(self):
        top = self.rect.top-500
        center = self.rect.centerx-5
        # center = self.rect.x + 35
        blust = Bluster(img_blast, center, top, 10, 600, 0)
        
        # blust = Bullet(img_bullet, self.rect.centerx, self.rect.top, 60, 200, -15)
        bullets.add(blust)


class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y > win_height:
            self.rect.x = randint(80, win_width - 80)
            self.rect.y = 0
            global lost
            lost = lost + 1


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


class Bluster(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
    

        


win_width = 1024
win_height = 720
display.set_caption('Space War')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
shoot_sound = mixer.Sound('bullet.mp3')
shoot_bluster_sound = mixer.Sound('bluster.mp3')
back_music = mixer.Sound('back_music.mp3')

ship = Player('ship.png', 5, win_height - 100, 80, 100, 10)

back_music.play(loops=-1)


bullets = sprite.Group()
enemys = sprite.Group()

for i in range(1, 6):
    enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
    enemys.add(enemy)

finish = False
blust_fire = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE and blust_fire == False:
                ship.fire()
                shoot_sound.play()
            if e.key == K_a:
                blust_fire = True
        elif e.type == KEYUP:
            if e.key == K_a:
                blust_fire = False

    if blust_fire:
        ship.fire_bluster()
        shoot_bluster_sound.play()
    else:
        pass
    
    if not finish:
        window.blit(background, (0, 0))
        # пишем текст на экране
        text = font.render("Счет: " + str(score), 1, (255, 255, 255))
        window.blit(text, (10, 20))
    
        text_lose = font.render("Пропущено: " + str(lost), 1, (255, 255, 255))
        window.blit(text_lose, (10, 50))

        bullets.draw(window)
        enemys.draw(window)
        ship.update()
        ship.reset()
        bullets.update()
        enemys.update()

        # при столкновении врагов с пулями, враги удаляются и их место занимают другие
        colides = sprite.groupcollide(enemys, bullets, True, True)
        for c in colides:
            score = score + 1
            enemy = Enemy(img_enemy, randint(80, win_width - 80), -40, 80, 50, randint(1, 5))
            enemys.add(enemy)
        
        # при столкновении врагов с кораблем, выводится текст GAMEOVER
        if sprite.spritecollide(ship, enemys, False) or lost >= 3:
            finish = True
            img = image.load('gameover.jpg')
            # d = img.get_width() // img.get_height()
            # window.fill((255,255,255))
            window.blit(transform.scale(img, (win_width, win_height)), (0, 0))
            back_music.stop()



        display.update()
    time.delay(40)
    