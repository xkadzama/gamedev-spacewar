from pygame import *
from os import path

mixer.init()


img_back = 'galaxy.png'
img_blast = 'blust.png'
img_bullet = 'bullet.png'


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
        bullet = Bullet(img_bullet, self.rect.right-20, self.rect.top, 15, 20, -15)
        bullet2 = Bullet(img_bullet, self.rect.left+5, self.rect.top, 15, 20, -15)
        bullets.add(bullet)
        bullets.add(bullet2)
    
    def fire_bluster(self):
        top = self.rect.top-500
        center = self.rect.centerx-5
        # center = self.rect.x + 35
        blust = Bluster(img_blast, center, top, 10, 600, 0)
        
        # blust = Bullet(img_bullet, self.rect.centerx, self.rect.top, 60, 200, -15)
        bullets.add(blust)

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Bluster(GameSprite):
    def update(self):
        if self.rect.y < 0:
            self.kill()
    

        


win_width = 700
win_height = 500
display.set_caption('Space War')
window = display.set_mode((win_width, win_height))
background = transform.scale(image.load(img_back), (win_width, win_height))
shoot_sound = mixer.Sound('bullet.mp3')
shoot_bluster_sound = mixer.Sound('bluster.mp3')
back_music = mixer.Sound('back_music.mp3')
ship = Player('ship.png', 5, win_height - 100, 80, 100, 10)
back_music.play(loops=-1)


bullets = sprite.Group()

blust_fire = False
run = True
while run:
    window.blit(background, (0, 0))
    
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

    bullets.draw(window)
    
    ship.update()
    ship.reset()
    bullets.update()
    
    time.delay(40)
    display.update()