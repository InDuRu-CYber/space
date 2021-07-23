from pygame import *
from random import randint
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self,player_image,player_x,player_y,player_speed, dimW, dimH):
        super().__init__()
        self.image=transform.scale(image.load(player_image),(dimW,dimH))
        self.speed=player_speed
        self.rect=self.image.get_rect()
        self.rect.x=player_x
        self.rect.y=player_y
    def reset(self):
        window.blit(self.image,(self.rect.x,self.rect.y ))

bullets=sprite.Group()

class Player (GameSprite):
    def move(self):
        keys=key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x=self.rect.x-self.speed
        
        if keys[K_d] and self.rect.x < win_width-100:
            self.rect.x=self.rect.x+self.speed

    def why_u_bullet_me(self):
        bullet=Bullet("bullet.png",self.rect.centerx,self.rect.top,10,20,20)
        bullets.add(bullet)

lives = 100 

class NPC(GameSprite):
    def update(self):
        global lives
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.x=randint(80,win_height-80)
            self.rect.y= 0
            lives -= 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed

        if self.rect.y < 0:
            self.kill()

class Asteroid(GameSprite):
    def update(self):
        global lives
        self.rect.y += self.speed
        if self.rect.y >= win_height:
            self.rect.x=randint(80,win_height-80)
            self.rect.y= 0

#le music
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
bullet=mixer.Sound('fire.ogg')

clock= time.Clock()
FPS= 60
step=6

win_width = 700
win_height=500
window=display.set_mode((700,500))
display.set_caption("headshot direct hit")
background=transform.scale(image.load("galaxy.jpg"),(700,500))
rocket=Player("rocket.png",250, 500-80 ,12,65,65)

asteroids = sprite.Group()
counter = 0 
while counter < 2:
    asteroid = Asteroid("asteroid.png", randint(80,win_width - 80), -80,randint(2,5), 80, 50)
    asteroids.add(asteroid)
    counter += 1

aliens=sprite.Group()
counter = 0
while counter < 5:
    alien = NPC("alien.png", randint(80,win_width - 80),-80,randint(2,3), 80, 50)
    aliens.add(alien)
    counter  += 1

score = 0

font.init()
font = font.SysFont('Arial',40)
text1 = font.render("Lives:" + str(lives),True, (255,255,255))
text2 = font.render("Score:" + str(score), True, (255, 129,80))

magazine = 0
reload = False

finish=False
run = True
text = font.render("Wait...",True,(255,0,0))
while run:
    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                
                if magazine < 10 and reload == False:
                    magazine += 1
                    rocket.why_u_bullet_me()
                    bullet.play()


                if magazine >= 10 and reload == False:
                    reload = True
                    start_reload_time = timer()

    if not finish:
        window.blit(background,(0,0))
        if reload == True:
            now = timer()

            if now - start_reload_time < 2:

                window.blit(text, (200,460))
            else:
                magazine = 0
                reload=False

        if lives <= 0:
            finish = True


        rocket.reset()
        aliens.update()
        rocket.move()
        asteroids.update()
        bullets.update()
        aliens.draw(window)
        asteroids.draw(window)
        display.update()
        bullets.draw(window)
        text1 = font.render("Lives:" + str(lives),True, (255,255,255))
        text2 = font.render("Score:" + str(score), True, (255, 129,80))
        window.blit(text1,(10,20))
        window.blit(text2,(10,60))
        
        accident=sprite.groupcollide(aliens,bullets, True , True)
        for col in accident:
            score +=1
            alien = NPC("alien.png", randint(80,win_width - 80),-80,randint(2,5), 80, 50)
            aliens.add(alien)
        
        if sprite.spritecollide(rocket,aliens,False):
            finish = True
            lose=font.render("The aliens defeated you" , True, (255, 0,80))
            window.blit(lose, (250,200))
        
        if sprite.spritecollide(rocket,asteroids,False):
            finish = True
            lose=font.render("Bonk" , True, (255, 0,80))
            window.blit(lose, (250,200))
        

        accident=sprite.groupcollide(asteroids,bullets, False , True)
        


        if score >= 20:
            finish=True
            win = font.render("Alien invasion stopped" , True, (255, 20,80))
            window.blit(win, (250,200))

    display.update()
    time.delay(20)