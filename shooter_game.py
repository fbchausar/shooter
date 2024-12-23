from pygame import *
from random import randint
from time import time as timer
#music.played
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
background_OST = mixer.Sound('space.ogg')
fire_sound = mixer.Sound('fire.ogg')
#picture
img_back = 'galaxy.jpg' 
img_hero = 'rocket.png'
img_enemy = 'ufo.png'
img_bullet = 'bullet.png'
img_ast = 'asteroid.png'
#win,lost,etc
lost = 0
goal = 10
score = 0
max_lost = 3
life = 3 

font.init()
font1 = font.Font(None,80)
win = font1.render('U WIN!',True,(255,255,255))
lose = font1.render('U LOSE!',True,(180,0,0))
font2 = font.Font(None,36)
#creating sprite and also a parent class
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,size_x,size_y,player_speed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y))
#enemy
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > win_height:
            self.rect.x = randint(80,win_width - 80)
            self.rect.y = 0 
            lost = lost+1 
# MC class
class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_RIGHT]and self.rect.x < win_width -80:
            self.rect.x +=self.speed
#method to shoot
    def fire(self):
        bullet = Bullet(img_bullet, self.rect.centerx, self.rect.top,15,20,-15)
        bullets.add(bullet)
#the bullet
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y <0:
            self.kill()


#create a small window for the game    
win_width = 700
win_height = 500
display.set_caption('Space Shooter')
window = display.set_mode((win_width,win_height))
background = transform.scale(image.load(img_back), (win_width,win_height))
#the sprite
ship = Player(img_hero,5,win_height - 100,80,100,10)

#creating an enemy group
monstre_group = sprite.Group()
for i in range(1,6):
    monstre = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
    monstre_group.add(monstre)

#creating asteroid(s)
asteroids = sprite.Group()
for i in range(1,3):
    asteroid = Enemy(img_ast,randint(30,win_width - 30),40,80,50,randint(1,7))
    asteroids.add(asteroid)

bullets = sprite.Group()

finish = False
run = True
rel_time = False
num_fire = 0

while run:
    #if the player click the exit button
    for e in event.get():
        if e.type == QUIT:
            run  = False
        #to shoot the bullet
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                if num_fire < 5 and rel_time == False:
                    num_fire = num_fire + 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    last_time = timer()
                    rel_time = True
    if not finish:
        window.blit(background,(0,0))
        

        asteroids.update()
        ship.update()
        asteroids.draw(window)
        bullets.update()
        ship.reset()
        monstre_group.update()
        monstre_group.draw(window)
        bullets.draw(window)
        #reload
        if rel_time == True:
            now_time = timer()

            if now_time - last_time <3:
                reload = font2.render('wait for a while, im reloading...',1,(150,0,0))
                window.blit(reload,(260,460))
            else:
                num_fire = 0
                rel_time = False
        collides = sprite.groupcollide(monstre_group,bullets,True,True )
        for c in collides:
            score = score +1
            monstre = Enemy(img_enemy,randint(80,win_width -80),-40,80,50,randint(1,5))
            monstre_group.add(monstre)
        if sprite.spritecollide(ship,monstre_group,False)or sprite.spritecollide(ship,asteroids,False):
            sprite.spritecollide(ship,monstre_group,True)
            sprite.spritecollide(ship,asteroids,True)
            life = life -1
        
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))
        
        if score >= goal:
            finish = True
            window.blit(win,(200,200))

        
        text = font2.render('score:' + str(score),1,(255,255,255))
        window.blit(text,(10,20))

        text_lose = font2.render('missed:'+str(lost),1,(255,255,255))
        window.blit(text_lose,(10,50))

        if life == 3:
            life_color = (0,150,0)
        if life == 2:
            life_color = (150,150,0)
        if life == 1:
            life_color = (150,0,0)
        
        display.update()
    else:
        finish = False
        score = 0
        lost = 0
        num_fire = 0
        life = 3
        for b in bullets:
            b.kill()
        for m in monstre_group:
            m.kill()
        for a in asteroids:
            a.kill()

        time.delay(3000)
        for i in range(1,6):
            monstre = Enemy(img_enemy,randint(80,win_width-80),-40,80,50,randint(1,5))
            monstre_group.add(monstre)
        for i in range(1,3):
            asteroid = Enemy(img_ast,randint(30,win_width-30),-40,80,50,randint(1,7))
    time.delay(50)





