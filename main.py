import asyncio
import pygame
import math
from pygame.locals import *
import sys
import os
import pygame.math 
import random
from pygame.math import Vector2
#---VARIABLE STORAGE--------------------------------------------------------------------------------->
pygame.mixer.pre_init(44100, 16, 2, 4096)
pygame.init()
vec = pygame.math.Vector2 

coins_collected = 0
birds_shot = 0
mini_bosses_defeated = 0
spikes_hit = 0
times_upgraded = 0


HEIGHT = 600
WIDTH = 880
ACC = 0.10
FRIC = -0.12
FPS = 60
d= 0
h = 0
clip = 8
money = 0
cost = 1
shotgun = False
upgrade_clicked = False
clicked = False
p_clicked = False
reduction = 0
pause = False
health = 5
game_done = False
add_money = 1
Start = False
high_score = 0
oldscore = 0
numbullets = 1
delay = 0
bosshealth = 8
bosskilled = False
removed_from_pause = False
score = 0
numtimes = 1
times = 1
t = 0
move = False
day = True
night = False
st = 0
orbit = 0
morning = False
boss = False
font = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 10)
import pickle
hiscore = 0

rects = []
flags = DOUBLEBUF
displaysurface = pygame.display.set_mode((WIDTH,HEIGHT))
FramePerSec = pygame.time.Clock()
pygame.display.set_caption("Capstone Game")
pygame.mouse.set_visible(False)
bulletsound = pygame.mixer.Sound(os.path.join('Sfx',"gunshot.ogg"))
shotgunsound = pygame.mixer.Sound(os.path.join('Sfx',"shotgun.ogg"))
moneysound = pygame.mixer.Sound(os.path.join('Sfx',"ka-ching.ogg"))
music = pygame.mixer.music.load(os.path.join('Sfx',"ForestWalk-320bit.ogg"))

reload = pygame.mixer.Sound(os.path.join('Sfx',"reload.ogg"))
pouring = pygame.mixer.Sound(os.path.join('Sfx',"pouring.ogg"))
damage = pygame.mixer.Sound(os.path.join('Sfx',"damage.ogg"))
birddeath = pygame.mixer.Sound(os.path.join('Sfx',"birddeath.ogg"))
upgrade = pygame.mixer.Sound(os.path.join('Sfx',"upgrade.ogg"))
rip = pygame.mixer.Sound(os.path.join('Sfx',"rip.ogg"))



#-----ENEMY_BULLET--------------------------------------------------->
class enemybullets(pygame.sprite.Sprite):
    def __init__(self):
        global clip
        global shotgun
        super().__init__()
        self.angle = math.atan((-M1.pos.y + P1.rect.y)/(-M1.pos.x + P1.rect.x))
        self.surf = pygame.transform.rotate(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'Bullet.png')).convert_alpha()), (10, 5)), - self.angle * 57.2958)
        self.speed = 8
        
        self.opposite = -1
        if (-M1.pos.x + P1.rect.x) > 0:
            self.opposite = 1
        self.pos = vec(M1.pos.x, M1.pos.y)
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
    def move(self): 

        self.rect.move_ip(self.speed *  math.cos(self.angle) * self.opposite, self.speed * math.sin(self.angle)*self.opposite)
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()
            

def enemybullet_gen(): 

    ebu  = enemybullets()
    ebu.rect.center = (M1.pos.x, M1.pos.y)
    enemybulletgroup.add(ebu)
    all_sprites.add(ebu)

#-----BULLET--------------------------------------------------->
class bullets(pygame.sprite.Sprite):
    def __init__(self):
        global clip
        global shotgun
        super().__init__()
        self.angle = math.atan((-P1.pos.y + A.rect.y)/(-P1.pos.x + A.rect.x))
        self.surf = pygame.transform.rotate(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'Bullet.png')).convert_alpha()), (10, 5)), - self.angle * 57.2958)
    
        self.speed = 8
        
        self.opposite = -1
        if (-P1.pos.x + A.rect.x) > 0:
            self.opposite = 1
        self.pos = vec(P1.pos.x, P1.pos.y)
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
    def move(self): 

        self.rect.move_ip(self.speed *  math.cos(self.angle) * self.opposite, self.speed * math.sin(self.angle)*self.opposite)
        if self.rect.left < 0 or self.rect.right > WIDTH or self.rect.top < 0 or self.rect.bottom > HEIGHT:
            self.kill()
            

def bullet_gen(): 

    bu  = bullets()
    bu.rect.center = (P1.pos.x, P1.pos.y)
    bulletgroup.add(bu)
    all_sprites.add(bu)
    if shotgun == True:
        bu  = bullets()
        bu.rect.center = (P1.pos.x, P1.pos.y)
        bulletgroup.add(bu)
        all_sprites.add(bu)
        bu.angle -=  57.2958 * 0.105
        bu  = bullets()
        bu.rect.center = (P1.pos.x, P1.pos.y)
        bulletgroup.add(bu)
        all_sprites.add(bu)
        bu.angle +=   57.2958 * 0.105
        bu  = bullets()
        bu.rect.center = (P1.pos.x, P1.pos.y)
        bulletgroup.add(bu)
        all_sprites.add(bu)


        

#-----CLOUDS--------------------------------------------------->
class clouds(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        n = 3.4
        self.cloud_list = []
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg.png')).convert_alpha()), (30*n, 19*n)))
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg1.png')).convert_alpha()), (59*n, 35*n)))
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg2.png')).convert_alpha()), (34*n, 23*n)))
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg3.png')).convert_alpha()), (50*n, 29*n)))
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg4.png')).convert_alpha()), (41*n, 28*n)))
        self.cloud_list.append(pygame.transform.scale((pygame.image.load(os.path.join('Images', 'sky_bg5.png')).convert_alpha()), (31*n, 24*n)))


        self.index = random.randrange(0, 5)
        self.surf = self.cloud_list[self.index]
        speed_list = [1, 2, 3, -1, -2, -3]
        self.speed = random.choice(speed_list)
        if self.speed < 0:
            self.pos = vec(random.randint(0, WIDTH),random.randint(0, HEIGHT))
        if self.speed > 0:
            self.pos = vec(random.randint(0, WIDTH),random.randint(0, HEIGHT))
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
    def move(self): 
        self.rect.move_ip(self.speed,0)

def cloud_gen(h):
    while len(cloudgroup) < 4 + h/3:
        co  = clouds()
        if co.speed < 0:
            co.pos = vec(random.randrange(WIDTH, WIDTH+1000),random.randrange(-HEIGHT, HEIGHT))
        if co.speed > 0:
            co.pos = vec(random.randrange(-1000, 0),random.randrange(-HEIGHT, HEIGHT))
        co.rect.center = (co.pos.x, co.pos.y)
        cloudgroup.add(co)
        all_sprites.add(co)
    
#------ISLAND--------------------------------------------------->

class island(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "floating island(1).png")).convert_alpha(), (350*0.65, 233*0.65))
        self.pos = vec((WIDTH/2, HEIGHT-75))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT-75))
    def move(self):
        pass
    
    
#--START------------------------------------------------------------->
class start_button(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        n = 4
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "Start.png")).convert_alpha(), (43*n, 9*n))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))
    def update(self):
        n = 4
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "Start.png")).convert_alpha(), (43*n, 9*n))
            self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "Start(1).png")).convert_alpha(), (43*n, 9*n))
            self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT/2))
    def move(self):
        pass

#--PAUSE------------------------------------------------------->
class pause_button(pygame.sprite.Sprite):
    global pause
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "play.png")).convert_alpha(), (50, 50))
        self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))
    def update(self):
        if pause == True:
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "play.png")).convert_alpha(),  (50, 50))
            self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))
        if pause == False:
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "pause.png")).convert_alpha(),  (50, 50))
            self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))
    def move(self):
        pass

class info_button(pygame.sprite.Sprite):
    global pause
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "information_icon.png")).convert_alpha(), (60, 60))
        self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))
    def update(self):
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "information_icon.png")).convert_alpha(),  (60, 60))
            self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', "information_icon(1).png")).convert_alpha(),  (60, 60))
            self.rect = self.surf.get_rect(center = (WIDTH - 50, 50))      
    
    def move(self):
        pass
        


#--SPEED UPGRADE----------------------------------------------------->

class speed_upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'speedometer icon.png')).convert_alpha(), (50, 50))
        self.rect = self.surf.get_rect(center = (WIDTH-70, HEIGHT-100))
    def update(self):
        global ACC
        global money
        global cost
        global score
        global reduction
        
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"speedometer icon.png")).convert_alpha(), (50, 50))
            self.rect = self.surf.get_rect(center = (WIDTH-70, HEIGHT-100))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"speedometer icon(1).png")).convert_alpha(), (50, 50))
            self.rect = self.surf.get_rect(center = (WIDTH-70, HEIGHT-100))
        global upgrade_clicked
        global times_upgraded
        if event.type == pygame.MOUSEBUTTONDOWN:
            upgrade_clicked = True
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos()) and money >= cost and upgrade_clicked == True:
            upgrade.play()
            upgrade_clicked = False
            ACC += 0.02
            money -= cost
            cost += 1
            score += 1000
            
            if reduction < 0.7:
                reduction += 0.15
            
    def move(self):
        pass



#--SHOTGUN UPGRADE----------------------------------------------------->

class shotgun_upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images','shotgun icon.png')).convert_alpha(), (57, 57))
        self.rect = self.surf.get_rect(center = (WIDTH-140, HEIGHT-100))
    def update(self):
        global ACC
        global money
        global cost
        global shotgun
        global score
        global event
        global times_upgraded
        yesshotgun = 0
        if shotgun == True:
            yesshotgun = 9994 - cost
        global upgrade_clicked
        if event.type == pygame.MOUSEBUTTONDOWN:
            upgrade_clicked = True
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos())and money >= (5 + yesshotgun + cost) and upgrade_clicked == True:
            upgrade.play()
            shotgun = True
            money -= (5 + cost + yesshotgun)
            cost += 1
            score += 1000
            times_upgraded += 1
            upgrade_clicked = False
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"shotgun icon.png")).convert_alpha(), (54, 54))
            self.rect = self.surf.get_rect(center = (WIDTH-140, HEIGHT-100))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"shotgun icon(1).png")).convert_alpha(), (54, 54))
            self.rect = self.surf.get_rect(center = (WIDTH-140, HEIGHT-100))
    def move(self):
        pass

#----------------------------------------------------------------------------------------------------->
class health_upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images','health icon.png')).convert_alpha(), (60, 60))
        self.rect = self.surf.get_rect(center = (WIDTH-210, HEIGHT-100))
    def update(self):
        global money
        global cost
        global health
        global score
        global upgrade_clicked
        global times_upgraded
        if event.type == pygame.MOUSEBUTTONDOWN:
            upgrade_clicked = True
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos())and money >= (2 + (cost-1)) and upgrade_clicked == True:
            upgrade.play()
            health += 1
            money -= (2 + (cost-1))
            cost += 1
            upgrade_clicked = False
            score += 1000
            times_upgraded += 1
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"health icon.png")).convert_alpha(), (60, 60))
            self.rect = self.surf.get_rect(center = (WIDTH-210, HEIGHT-100))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"health icon(1).png")).convert_alpha(), (60, 60))
            self.rect = self.surf.get_rect(center = (WIDTH-210, HEIGHT-100))
    def move(self):
        pass
#--------------------------------------------------------------------------------------->
class money_upgrade(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images','money icon.png')).convert_alpha(), (53, 53))
        self.rect = self.surf.get_rect(center = (WIDTH-280, HEIGHT-105))
    def update(self):
        global money
        global cost
        global score
        global add_money
        global upgrade_clicked
        global times_upgraded
        if event.type == pygame.MOUSEBUTTONDOWN:
            upgrade_clicked = True
        if event.type == pygame.MOUSEBUTTONUP and self.rect.collidepoint(pygame.mouse.get_pos())and money >= (1 + cost*2) and upgrade_clicked == True:
            upgrade.play()
            add_money += 1
            money -= (1 + cost*2)
            cost += 1
            score += 1000
            upgrade_clicked = False
            times_upgraded += 1
        if not self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"money icon.png")).convert_alpha(), (53, 53))
            self.rect = self.surf.get_rect(center = (WIDTH-280, HEIGHT-105))
        if self.rect.collidepoint(pygame.mouse.get_pos()):
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"money icon(1).png")).convert_alpha(), (53, 53))
            self.rect = self.surf.get_rect(center = (WIDTH-280, HEIGHT-105))
    def move(self):
        pass
#-----SUN MOON------------------------------------------------>

class sunmoon(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images','moon.png')).convert_alpha(), (53, 53))
        self.rect = self.surf.get_rect(center = (0, HEIGHT/2))
        self.acc = vec(0,0)
        self.pos = vec((WIDTH/2, 100))
        self.vel = vec(0,0)


    def move(self):
        global orbit
        if day == True and night == False and morning == True and self.pos.x > WIDTH:
            self.pos = vec((0, HEIGHT/2))
            orbit = 0.5
        if Start == True:
            self.pos.x += 0.7
            self.pos.y -= orbit
        if Start == False:
            self.pos.x += 0.35
            self.pos.y -= orbit/2
        self.rect.midbottom = self.pos


 

#---CROSSHAIRS----------------------------------------------------------------------------------->

class crosshairs(pygame.sprite.Sprite):
    def __init__(self):
        global shotgun
        s = 1
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"pixelCROSSHAIR.png")).convert_alpha(), (20, 20))
        self.rect = self.surf.get_rect()
    def update(self):
        self.rect.center = pygame.mouse.get_pos()
        if shotgun == True:
            self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"pixelCROSSHAIR.png")).convert_alpha(), (20, 20))
            self.rect = self.surf.get_rect()
            self.rect.center = pygame.mouse.get_pos()
    def move(self):
        pass
    
#---BOSS_ONE-------------------------------------------------------------------------------->

class Mirror(pygame.sprite.Sprite):
    def __init__(self):
        xp = 60
        yp = 60
        super().__init__()
        self.enemy_png_R = []
        self.enemy_png_R.append(pygame.image.load(os.path.join('Images',"boss1.png")).convert_alpha())
        self.enemy_png_R.append(pygame.image.load(os.path.join('Images','boss2.png')).convert_alpha())
        self.enemy_png_R.append(pygame.image.load(os.path.join('Images','boss3.png')).convert_alpha())
        self.enemy_png_R.append(pygame.image.load(os.path.join('Images','boss4.png')).convert_alpha())
        self.enemy_png_R.append(pygame.image.load(os.path.join('Images','boss5.png')).convert_alpha())
        self.enemy_png_L = []
        self.enemy_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','boss1.png')).convert_alpha(), True, False))
        self.enemy_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','boss2.png')).convert_alpha(), True, False))
        self.enemy_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','boss3.png')).convert_alpha(), True, False))
        self.enemy_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','boss4.png')).convert_alpha(), True, False))
        self.enemy_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','boss5.png')).convert_alpha(), True, False))
        self.index = 0

        self.surf = self.enemy_png_R[self.index]
        self.rect = Rect(WIDTH - P1.pos.x, HEIGHT - P1.pos.y, 30, 50)
        self.hitbox = self.rect
        self.pos = vec((WIDTH - P1.pos.x, HEIGHT - P1.pos.y))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def update_right(self):
        self.index += 1
        if self.index >= len(self.enemy_png_R):
            self.index = 0
        self.surf = self.enemy_png_R[self.index]
    def update_left(self):
        self.index += 1
        if self.index >= len(self.enemy_png_L):
            self.index = 0
        self.surf = self.enemy_png_L[self.index]
    def move(self):
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_a]:
            move = True
            self.acc.x = ACC 
            self.update_right()
        if pressed_keys[K_d]:
            move = True
            self.acc.x = -ACC 
            self.update_left()
        self.rect.midbottom = (WIDTH - P1.pos.x, HEIGHT - P1.pos.y)
        self.pos = vec(WIDTH - P1.pos.x, HEIGHT - P1.pos.y) 
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0




#---PLAYER----------------------------------------------------------------------------------->


class Player(pygame.sprite.Sprite):
    def __init__(self):
        xp = 60
        yp = 60
        super().__init__()
        self.player_png_R = []
        self.player_png_R.append(pygame.image.load(os.path.join('Images',"pxArt (Balloon1).png")).convert_alpha())
        self.player_png_R.append(pygame.image.load(os.path.join('Images','pxArt (Balloon2).png')).convert_alpha())
        self.player_png_R.append(pygame.image.load(os.path.join('Images','pxArt (Balloon3).png')).convert_alpha())
        self.player_png_R.append(pygame.image.load(os.path.join('Images','pxArt (Balloon3).png')).convert_alpha())
        self.player_png_R.append(pygame.image.load(os.path.join('Images','pxArt (Balloon5).png')).convert_alpha())
        self.player_png_L = []
        self.player_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','pxArt (Balloon1).png')).convert_alpha(), True, False))
        self.player_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','pxArt (Balloon2).png')).convert_alpha(), True, False))
        self.player_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','pxArt (Balloon3).png')).convert_alpha(), True, False))
        self.player_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','pxArt (Balloon4).png')).convert_alpha(), True, False))
        self.player_png_L.append(pygame.transform.flip(pygame.image.load(os.path.join('Images','pxArt (Balloon5).png')).convert_alpha(), True, False))
        self.index = 0

        self.surf = self.player_png_R[self.index]
        self.rect = Rect(WIDTH/2, HEIGHT/2, 30, 50)
        self.hitbox = self.rect
        self.pos = vec((WIDTH/2, HEIGHT/2))
        self.vel = vec(0,0)
        self.acc = vec(0,0)
    def update_right(self):
        self.index += 1
        if self.index >= len(self.player_png_R):
            self.index = 0
        self.surf = self.player_png_R[self.index]
    def update_left(self):
        self.index += 1
        if self.index >= len(self.player_png_L):
            self.index = 0
        self.surf = self.player_png_L[self.index]
    def move(self):
        global move
        self.acc = vec(0, 0.03)
        pressed_keys = pygame.key.get_pressed()            
        if pressed_keys[K_a]:
            move = True
            self.acc.x = -ACC 
            self.update_left()
        if pressed_keys[K_d]:
            move = True
            self.acc.x = ACC 
            self.update_right()
        if pressed_keys[K_w] and G.pos.x > -WIDTH/2:
            move = True
            self.acc.y = -ACC
        if pressed_keys[K_s] and G.pos.x > -WIDTH/2:
            move = True
            self.acc.y = ACC

        self.acc.x += self.vel.x * FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
         
        if self.pos.x > WIDTH:
            self.pos.x = WIDTH
        if self.pos.x < 0:
            self.pos.x = 0
            
        self.rect.midbottom = self.pos
    def ammocollect(self):
        global clip
        collect = pygame.sprite.spritecollide(P1 ,ammunition, False)
        
        if collect:
            for entity in ammunition:
                reload.play()
                entity.kill()
                clip += 4
    def ground(self):
        global score
        hits = pygame.sprite.spritecollide(P1 ,objects, False)
        if hits:
            self.pos.y = hits[0].rect.top + 1
            self.vel.y = -1
            score -= 1000
            
            
#------COIN PICKUP----------------------------------------------------------------------------------->
class coins(pygame.sprite.Sprite):
    def __init__(self):
        bx = 30
        by = 30
        super().__init__()
        self.coin_png_L = []
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin1.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin2.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin3.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin4.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin5.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin6.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin7.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin8.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin9.png')).convert_alpha(), True, False)), (bx, by)))
        self.coin_png_L.append(pygame.transform.scale((pygame.transform.flip(pygame.image.load(os.path.join('Images','coin10.png')).convert_alpha(), True, False)), (bx, by)))
  
    
        self.index = 0
        self.surf = self.coin_png_L[self.index]
        self.pos = vec(random.randint(0, WIDTH), 0)
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
        self.speed = 2
        self.moving = True
    def update_left(self):
        self.index += 1
        if self.index >= len(self.coin_png_L):
            self.index = 0
        self.surf = self.coin_png_L[self.index]    
    
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(0, self.speed)
def coin_gen():
    while len(coingroup) < 5 :
        width = random.randrange(50,100)
        c = coins()             
        C = True
       
        while C:
             c = coins()
             c.pos.x = random.randint(0, WIDTH)
             c.pos.y = random.randint(0, 70)
             c.rect.center = (c.pos.x, c.pos.y)
             C = check(c, coingroup)
        coingroup.add(c)
        all_sprites.add(c)
#-----MOUSE----------------------------------------------------------------------------------------------->
class mouse(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"MOUSE.png")).convert_alpha(), (21*4,25*4)))
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"MOUSE(2).png")).convert_alpha(), (21*4,25*4)))
        
        self.index = 0
        self.surf = self.frames[self.index]
        self.rect = self.surf.get_rect(center =(WIDTH/2 + 150, 3*HEIGHT/4))
    def update(self):
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
            self.surf = self.frames[self.index]
#-----WASD----------------------------------------------------------------------------------------------->
class wasd(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.frames = []
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"WASD.png")).convert_alpha(), (32*4,21*4)))
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"WASD(1).png")).convert_alpha(), (32*4,21*4)))
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"WASD(2).png")).convert_alpha(), (32*4,21*4)))
        for i in range(50):
            self.frames.append(pygame.transform.scale(pygame.image.load(os.path.join('Images',"WASD(3).png")).convert_alpha(), (32*4,21*4)))
        
        self.index = 0
        self.surf = self.frames[self.index]
        self.rect = self.surf.get_rect(center =(WIDTH/2 -150, 3*HEIGHT/4))
    def update(self):
            self.index += 1
            if self.index >= len(self.frames):
                self.index = 0
            self.surf = self.frames[self.index]


#-----BIRD ENEMY----------------------------------------------------------------------------------------------->
class birds(pygame.sprite.Sprite):
    def __init__(self):
        s = 90
        bx = s
        by = s
        super().__init__()
        self.bird_png_L2 = []

        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird3a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird3a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird3a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird8a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird8a.png')).convert_alpha()), (bx, by)))
        self.bird_png_L2.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird8a.png')).convert_alpha()), (bx, by)))



        self.bird_png_L3 = []
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird1.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird2.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird3.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird3.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird4.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird5.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird6.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird7.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird8.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird9.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird9.png')).convert_alpha()), (bx, by)))
        self.bird_png_L3.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','bird9.png')).convert_alpha()), (bx, by)))
        self.bird_png_L = random.choice([self.bird_png_L2, self.bird_png_L3])
        self.index = 0
        self.surf = self.bird_png_L[self.index]
        speed_list = [2, -2, 3, -3, 4, -4]
        self.speed = random.choice(speed_list)*1.5
        if self.speed < 0:
            self.pos = vec(random.randint(WIDTH, WIDTH+200),0)
        if self.speed > 0:
            self.pos = vec(random.randint(-200, 0),0)
        self.rect = self.surf.get_rect(center = (self.pos.x, self.pos.y))
        self.moving = True
    def update_left(self):
        if self.moving == True:
            self.index += 1
            if self.index >= len(self.bird_png_L):
                self.index = 0
            self.surf = self.bird_png_L[self.index]
            self.surf = pygame.transform.flip(self.bird_png_L[self.index], True, False)
    def update_right(self):
        if self.moving == True:
            self.index += 1
            if self.index >= len(self.bird_png_L):
                self.index = 0
            self.surf = self.bird_png_L[self.index]
    def move(self):
        if self.moving == True:  
            self.rect.move_ip(self.speed,0)
        else:
            self.rect.move_ip(0, 5)
    def shot(self):
        global score
        global clip
        global shotgun
        
        if self.bird_png_L == self.bird_png_L2 and self.speed > 0:
            self.surf = pygame.transform.rotate(pygame.transform.flip(self.bird_png_L2[17], True, False), 180)
        if self.bird_png_L == self.bird_png_L2 and self.speed < 0:
            self.surf = pygame.transform.rotate(self.bird_png_L2[17], 180)
        if self.bird_png_L == self.bird_png_L3 and self.speed > 0:
            self.surf = pygame.transform.rotate(pygame.transform.flip(self.bird_png_L3[16], True, False), 180)
        if self.bird_png_L == self.bird_png_L3 and self.speed < 0:
            self.surf = pygame.transform.rotate(self.bird_png_L3[16], 180)
        self.moving = False
        
        """
        if shotgun == False:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(pygame.mouse.get_pos()) and clip > 0:
                self.kill()
                score += 400

        if shotgun == True:
            if event.type == pygame.MOUSEBUTTONDOWN and self.rect.colliderect(A.rect) and clip > 0:
                self.kill()
                score += 400"""

        
def bird_gen(h):
    while len(birdgroup) < 1 + h/3:
        width = random.randrange(50,100)
        b  = birds()             
        C = True
       
        while C:
             b = birds()
             if b.speed < 0:
                b.pos = vec(WIDTH ,random.randrange(0, 300))
             if b.speed > 0:
                b.pos = vec(0 ,random.randrange(0, 300))
             b.rect.center = (b.pos.x, b.pos.y)
             C = check(b, birdgroup)
        birdgroup.add(b)
        all_sprites.add(b)
#----PLATFORM---------------------------------------------------------------------------------> 
class platform(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface(((WIDTH/2 -140)*0.65, 20*0.65))
        self.surf = self.surf.convert_alpha()
        self.surf.fill((0, 0, 0, 0))
        self.pos = vec((WIDTH/2, HEIGHT - 90))
        self.rect = self.surf.get_rect(center = (WIDTH/2, HEIGHT - 90))
    def move(self):
        pass
#----SPIKE OBSTACLE----------------------------------------------------------------------------------->
class spikes(pygame.sprite.Sprite):
    def __init__(self):
        s = 70
        global health
        super().__init__()
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"pxArt (3).png")).convert_alpha(), (s, s))
        #self.surf = pygame.Surface((30, 30))
        #self.surf.fill((255,0,0))s
        self.index = 0
        self.was_hit = False
        self.boom_L = []
        self.boom = False
        for i in range(5):
            self.boom_L.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','boom1.png')).convert_alpha()), (s*1.3, s*1.3)))
        for i in range(5):
            self.boom_L.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','boom2.png')).convert_alpha()), (s*1.3, s*1.3)))
        for i in range(5):
            self.boom_L.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','boom3.png')).convert_alpha()), (s*1.3, s*1.3)))
        for i in range(5):
            self.boom_L.append(pygame.transform.scale((pygame.image.load(os.path.join('Images','boom4.png')).convert_alpha()), (s*1.3, s*1.3)))
        self.rect = Rect(random.randint(0,WIDTH-10),random.randint(0, 200), 50, 50)
    def move(self):
        pass
    def update(self):
        global health
        global spikes_hit
        global score
        if self.was_hit == True:
            if self.index == 0:
                damage.play()               
                health -= 1
                spikes_hit += 1
                score -= 2500

            self.index += 1
            if self.index >= len(self.boom_L):
                self.index = 0
                
                self.kill()
            self.surf = self.boom_L[self.index]



def check(spikes, groupies):
    if pygame.sprite.spritecollideany(spikes,groupies):
        return True
    else:
        for entity in groupies:
            if entity == spikes:
                continue
            if (abs(spikes.rect.top - entity.rect.bottom) < 40) and (abs(spikes.rect.bottom - entity.rect.top) < 40):
                return True
        C = False
        
def spike_gen(h):
    while len(obstacles) < 7 +h/3:
        width = random.randrange(50,100)
        C = True
         
        while C:
             s1 = spikes()
             s1.rect.center = (random.randrange(0, WIDTH - width),random.randrange(-HEIGHT, 0))
             C = check(s1, obstacles)
        obstacles.add(s1)
        all_sprites.add(s1)    

#----CAN OF GAS PICKUP---------------------------------------------------------------------------------------->
class can(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((30, 30))
        #self.surf.fill((0,0,255))
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"pxArt (4).png")).convert_alpha(), (40, 40))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, 200)))
    def move(self):
        pass

def can_gen():
    while len(pickup) < 1 :
        width = random.randrange(50,100)
        c1  = can()             
        c1.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
        pickup.add(c1)
        all_sprites.add(c1)
#--------------AMMO--------------------------------------------------------------------------------------------->
class ammo(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #self.surf = pygame.Surface((30, 30))
        #self.surf.fill((0,0,255))
        self.surf = pygame.transform.scale(pygame.image.load(os.path.join('Images',"ammo sprite.png")).convert_alpha(), (40, 40))
        self.rect = self.surf.get_rect(center = (random.randint(0,WIDTH-10),
                                                 random.randint(0, 200)))
    def move(self):
        pass

def ammo_gen():
    while len(ammunition) < 1 :
        width = random.randrange(50,100)
        a  = ammo()             
        a.rect.center = (random.randrange(0, WIDTH - width),
                             random.randrange(-50, 0))
        ammunition.add(a)
        all_sprites.add(a)
#---GAS BAR--------------------------------------------------------------------------------->

class gas(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__() 
        self.surf = pygame.Surface((WIDTH, 20))
        self.surf.fill((255,255,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, 10))
   
        self.pos = vec((WIDTH/2, 10))
        self.vel = vec(0,0)
        self.acc = vec(0,0)



    def move(self):
        self.acc = vec(0,0)
    
        pressed_keys = pygame.key.get_pressed()
        if pressed_keys[K_w] or pressed_keys[K_a] or pressed_keys[K_d]:
            self.pos.x -= (0.8 - reduction)
        if not pressed_keys[K_w] or pressed_keys[K_a] or pressed_keys[K_d] and self.pos.x < WIDTH/2 - 8:
            self.pos.x += 0
        
        
        self.rect.midbottom = self.pos
        collect = pygame.sprite.spritecollide(P1 ,pickup, False)
        
        if collect:
            for entity in pickup:
                pouring.play()
                entity.kill()
                self.pos.x += WIDTH/3
        if self.pos.x > WIDTH/2:
            self.pos.x = WIDTH/2


#--HEALTH BAR--------------------------------------------------------------------------------->

class healthbar(pygame.sprite.Sprite):
    def __init__(self):
        self.amount = 5
        super().__init__() 
        self.surf = pygame.Surface((WIDTH, 10))
        self.surf.fill((255, 0,0))
        self.rect = self.surf.get_rect(center = (WIDTH/2, 20))
   
        self.pos = vec((WIDTH/2, 20))
        self.vel = vec(0,0)
        self.acc = vec(0,0)



    def move(self):
        pass
    def update(self):
        if bosshealth > self.amount:
            self.amount = bosshealth 
        self.rect.x -= WIDTH/self.amount

#-------ENTITY GENERATION----------------------------------------------------------------------------->
PT1 = platform()
P1 = Player()
G = gas()
A = crosshairs()
sm = sunmoon()
c1 = can()
a = ammo()
S = shotgun_upgrade()
H = health_upgrade()
land = island()
moneyup = money_upgrade()
upgrade1 = speed_upgrade()
all_sprites = pygame.sprite.Group()
all_sprites.add(P1)
all_sprites.add(PT1)
all_sprites.add(G)
all_sprites.add(c1)
all_sprites.add(A)
all_sprites.add(a)
all_sprites.add(sm)
all_sprites.add(land)
objects = pygame.sprite.Group()
objects.add(PT1)

obstacles = pygame.sprite.Group()
obstacles.add(PT1)
pickup = pygame.sprite.Group()
pickup.add(c1)
ammunition = pygame.sprite.Group()
ammunition.add(a)

birdgroup = pygame.sprite.Group()
coingroup = pygame.sprite.Group()
bulletgroup = pygame.sprite.Group()
enemybulletgroup = pygame.sprite.Group()
cloudgroup = pygame.sprite.Group() 
M1 = Mirror()


for x in range(random.randint(2,3)):
    C = True
    b = birds()
    while C:
        b = birds()
        C = check(b, birdgroup)
    birdgroup.add(b)
    all_sprites.add(b)

for x in range(1):
    c = coins()
    coingroup.add(c)
    all_sprites.add(c)

for x in range(random.randint(4,5)):
    C = True
    s = spikes()
    while C:
        s = spikes()
        C = check(s, obstacles)
    obstacles.add(s)
    all_sprites.add(s)


all_sprites.add(upgrade1)
all_sprites.add(S)
all_sprites.add(H)
all_sprites.add(moneyup)
bg = pygame.transform.scale(pygame.image.load(os.path.join('Images',"sky.png")).convert(),(WIDTH, HEIGHT))
sunset = pygame.transform.scale(pygame.image.load(os.path.join('Images',"sunset.jpg")).convert(),(WIDTH, HEIGHT))
dg = pygame.transform.scale(pygame.image.load(os.path.join('Images', 'black.jpg')).convert(),(WIDTH, HEIGHT))
sunset.set_alpha(st)
dg.set_alpha(t)



#----KILL FUNCTION----------------------------------------------------------------------------------------->
"""def game_over():

    pressed_keys = pygame.key.get_pressed() 
    while game_done == True:
        #for entity in all_sprites:
            #entity.kill()
        displaysurface.fill((255,0,0))
        f = pygame.font.SysFont("Impact", 60)
        g  = f.render("Your Score:", True, (0,0,0))   
        displaysurface.blit(g, (WIDTH/2 - 120, HEIGHT/2))
        s = f.render(str(score), True, (0,0,0))
        displaysurface.blit(s, (WIDTH/2 - 12.5 * (len(str(score))-1), HEIGHT/2 + 200))
        pygame.display.update()
        if pressed_keys[K_SPACE]:
            game_done = False
            break
        #time.sleep(10)
        #pygame.quit()
        #sys.exit()
"""
def for_group_above_height(group):
    for entity in group:
        entity.rect.y += abs(P1.vel.y)
        if entity.rect.top >= HEIGHT:
            entity.kill()

def for_group_below_height(group):
    for entity in group:
        entity.kill()
    
#----MAIN GAME LOOP---------------------------------------------------------------------------------------->




async def main():
    
    global M1
    global PT1
    global P1 
    global G
    global bg
    global A 
    global sm 
    global c1
    global a 
    global S
    global H 
    global land 
    global moneyup
    global times
    global upgrade1 
    global all_sprites
    global objects

    global obstacles 
    global pickup 
    global ammunition
    global cloudgroup
    global birdgroup 
    global coingroup
    global bulletgroup
    global enemybulletgroup 
    global HEIGHT 
    global WIDTH
    global ACC 
    global FRIC 
    global FPS 
    global d
    global h  
    global clip 
    global money 
    global cost 
    global shotgun 
    global clicked 
    global p_clicked 
    global pause 
    global health
    global game_done 
    global add_money 
    global Start 
    global high_score 
    global oldscore
    global numbullets
    global delay 
    global bosshealth
    global bosskilled 
    global score
    global t 
    global day
    global night 
    global st 
    global orbit 
    global morning 
    global boss 
    global font
    global event
    global hiscore
    global info_b
    global reduction
    global numtimes
    global coins_collected 
    global birds_shot 
    global mini_bosses_defeated 
    global spikes_hit 
    global times_upgraded 
    while True:
        pygame.mixer.music.play(-1)
        sm = sunmoon()
        PT1 = platform()
        P1 = Player()
        pause_b = pause_button()
        info_b = info_button()
        G = gas()
        A = crosshairs()
        c1 = can()
        land = island()
        a = ammo()
        S = shotgun_upgrade()
        H = health_upgrade()
        moneyup = money_upgrade()
        upgrade1 = speed_upgrade()
        
        all_sprites = pygame.sprite.Group()
        all_sprites.add(sm)
        all_sprites.add(land)
        all_sprites.add(P1)
        
        
        
        all_sprites.add(PT1)
        all_sprites.add(G)
        all_sprites.add(c1)
        all_sprites.add(A)
        all_sprites.add(a)
        
        for sprite in all_sprites:
            rects.append(sprite)
        objects = pygame.sprite.Group()
        objects.add(PT1)
        obstacles = pygame.sprite.Group()
        pickup = pygame.sprite.Group()
        pickup.add(c1)
        ammunition = pygame.sprite.Group()
        ammunition.add(a)
        islands = pygame.sprite.Group()
        islands.add(land)
        islands.add(PT1)
        birdgroup = pygame.sprite.Group()
        coingroup = pygame.sprite.Group()
        cloudgroup = pygame.sprite.Group()
        bulletgroup = pygame.sprite.Group()
        all_sprites.add(info_b)

        for x in range(random.randint(2,3)):
            C = True
            b = birds()
            while C:
                b = birds()
                C = check(b, birdgroup)
            birdgroup.add(b)
            all_sprites.add(b)

        for x in range(1):
            c = coins()
            coingroup.add(c)
            all_sprites.add(c)

        for x in range(random.randint(4,5)):
            C = True
            s = spikes()
            while C:
                s = spikes()
                C = check(s, obstacles)
            obstacles.add(s)
            all_sprites.add(s)


        all_sprites.add(upgrade1)
        all_sprites.add(S)
        all_sprites.add(H)
        all_sprites.add(moneyup)
        all_sprites.add(pause_b)
        start_b = start_button()
        buttons = wasd()
        mouse_buttons = mouse()

        while Start == False: 
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            buttons.update()
            mouse_buttons.update()
            info_b.update()
            start_b.update()
            displaysurface.blit(bg,(0,0))
            displaysurface.blit(sm.surf, sm.rect)
            sm.move()
            displaysurface.blit(sunset,(0,0))
            displaysurface.blit(dg,(0,0))
            displaysurface.blit(A.surf, A.rect)
            displaysurface.blit(start_b.surf, start_b.rect)
            displaysurface.blit(info_b.surf, info_b.rect)
            displaysurface.blit(buttons.surf, buttons.rect)
            displaysurface.blit(mouse_buttons.surf, mouse_buttons.rect)
            f = n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 7)   
            if hiscore < 25000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"silhouette.png")).convert_alpha(), (30, 50)), (30, 30))
            if hiscore > 25000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"Bronze.png")).convert_alpha(), (30, 50)), (30, 30))
            g  = f.render("25K pts", True, (0,0,0))   
            displaysurface.blit(g, (20, 15))
            if hiscore < 35000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"silhouette.png")).convert_alpha(), (30, 50)), (90, 30))
            if hiscore > 35000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"Silver.png")).convert_alpha(), (30, 50)), (90, 30))
            g  = f.render("35K pts", True, (0,0,0))   
            displaysurface.blit(g, (80, 15))
            if hiscore < 45000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"silhouette.png")).convert_alpha(), (30, 50)), (150, 30))
            if hiscore > 45000:
                displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"Gold.png")).convert_alpha(), (30, 50)), (150, 30))
            g  = f.render("45K pts", True, (0,0,0))   
            displaysurface.blit(g, (140, 15))
            f = n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 10)
            g  = f.render("A game by CasualIntellectual", True, (0,0,0))   
            displaysurface.blit(g, (WIDTH/2 - 145, HEIGHT/2 + 60))
            f = n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 10)
            g  = f.render("WASD to move", True, (0,0,0))   
            displaysurface.blit(g, (WIDTH/2 -210, HEIGHT/2 + 220))
            g  = f.render("R-click to shoot/select", True, (0,0,0))   
            displaysurface.blit(g, (WIDTH/2 + 50, HEIGHT/2 + 220))
            if event.type == pygame.MOUSEBUTTONDOWN and info_b.rect.collidepoint(pygame.mouse.get_pos()): 
                g  = f.render("Music: 'Forest Walk' by Alexander Nakarada", True, (0,0,0))   
                displaysurface.blit(g, (WIDTH/2 - 150, HEIGHT/2 - 280))
                g  = f.render("Art: BDragon1727 (Explosion) and LateNightCoffee (Clouds)", True, (0,0,0))
                g_rect = g.get_rect(center=(WIDTH/2 + 50, HEIGHT/2 - 257))
                displaysurface.blit(g, g_rect)
                g  = f.render("SFX: mixkit", True, (0,0,0))
                g_rect = g.get_rect(center=(WIDTH/2 + 50, HEIGHT/2 - 240))
                displaysurface.blit(g, g_rect)
            displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"Title.png")).convert_alpha(), (172*4,18*4)), (100, HEIGHT/4))
            
           

            pygame.display.update()
            
            A.move()
            A.update()
            start_b.update()
            if pause == False:
                if day == True and morning == False and night == False:
                    st += 0.5
                    if st > 600:
                        day = False
                        night = True
                if day == True and morning == True and night == False:
                    st -= 0.5
                    if st == 0:
                        morning = False
                        night == True
                        st = -100
                    
                if day == False and night == True:
                    t += 0.25
                    if t > 200:
                        day = True
                    
                if day == True and night == True:
                    t -= 0.25
                    if t <= 0:
                        morning = True
                        night = False
            
            dg.set_alpha(t)
            sunset.set_alpha(st/4)
            if event.type == pygame.MOUSEBUTTONUP and start_b.rect.collidepoint(pygame.mouse.get_pos()):
                start_b.kill()
                info_b.kill()
                Start = True
            if orbit <= 0:
                orbit -= 0.0023/5
            if orbit > 0:
                orbit -= 0.0023/5
            
            await asyncio.sleep(0)
        t = 0
        day = True
        night = False
        st = 0
        orbit = 0
        morning = False
        sm.pos = vec((WIDTH/2, 100))


        while game_done == False:
            
            if event.type == pygame.MOUSEBUTTONDOWN and pause_b.rect.collidepoint(pygame.mouse.get_pos()):
                p_clicked = True

            if event.type == pygame.MOUSEBUTTONUP and p_clicked == True:
                
                if pause == False:
                    pause = True
                elif pause == True:
                    pause = False
                p_clicked = False
            

                
                
                


            pause_b.update()
            
            
            if pause == False:    
                if day == True and morning == False and night == False:
                    st += 1
                    if st > 600:
                        day = False
                        night = True
                if day == True and morning == True and night == False:
                    st -= 1
                    if st == 0:
                        morning = False
                        night == True
                        st = -100
                    
                if day == False and night == True:
                    t += 0.5
                    if t > 200:
                        day = True
                    
                if day == True and night == True:
                    t -= 0.5
                    if t <= 0:
                        morning = True
                        night = False
                    
            dg.set_alpha(t)
            sunset.set_alpha(st/4)
            start_b.kill()
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            if pause == False:
                for bird in birdgroup:

                    if bird.speed < 0:
                        bird.update_left()
                    if bird.speed > 0:
                        bird.update_right()
                    if bird.rect.right <= 0:
                        bird.kill()
                    if bird.rect.left >= WIDTH:
                        bird.kill()
            if event.type == pygame.MOUSEBUTTONDOWN and pause == False:
                
                clicked =  True
                
                
            if event.type == pygame.MOUSEBUTTONUP and clicked == True and clip > 0 and pause == False:

                if clip > 0 and not pygame.Rect.colliderect(A.rect, upgrade1.rect) and not  pygame.Rect.colliderect(A.rect, S.rect) and not pygame.Rect.colliderect(A.rect, H.rect) and not pygame.Rect.colliderect(A.rect, moneyup.rect) and not pygame.Rect.colliderect(A.rect, pause_b.rect):
                    if shotgun == False:
                        bullet_gen()
                        bulletsound.play()
                    if shotgun == True:
                        bullet_gen()
                        shotgunsound.play()
                if not pygame.Rect.colliderect(A.rect, pause_b.rect):
                    clip -= 1
                clicked = False        
                        
            if orbit <= 0:
                orbit -= 0.005/5.7
            if orbit > 0:
                orbit -= 0.005/5.7
            if pause == False:
                for coin in coingroup:
                    coin.update_left()

            displaysurface.blit(bg,(0,0))
            displaysurface.blit(sunset,(0,0))
            sunset.set_alpha(st/4)
            displaysurface.blit(sm.surf, sm.rect)
            for entity in all_sprites:
                displaysurface.blit(entity.surf, entity.rect)
                if pause == False and entity != P1:
                    entity.move()
            P1.ground()
            
            A.update()
            P1.ammocollect()
            if P1.rect.top <= HEIGHT / 5 and pause == False:
                score += 25
                P1.pos.y += abs(P1.vel.y)
                for spike in obstacles:
                    spike.rect.y += abs(P1.vel.y)
                    if spike.rect.top >= HEIGHT:
                        spike.kill()
                for I in islands:
                    I.rect.y += abs(P1.vel.y)
                    
                
                for_group_above_height(pickup)
                for_group_above_height(ammunition)
                for_group_above_height(birdgroup)
                for_group_above_height(coingroup)
                for_group_above_height(cloudgroup)
                

            for clo in cloudgroup:
                if clo.rect.right <= 0:
                    clo.kill()
                if clo.rect.left >= WIDTH:
                    clo.kill()
                covered = pygame.Rect.colliderect(clo.rect, P1.rect)
                if covered:
                    displaysurface.fill((255, 255, 255, 100))
            if pause == False:
                if score >= 20000*times and boss == True and bosskilled == True:
                    boss = False
                    bosskilled = False
                    bosshealth = 8 + times
                    
            if pause == False:
                if score >= 20000*times and boss == False and bosskilled == False:
                    Health_bar = healthbar()  
                    M1 = Mirror()
                    all_sprites.add(M1)
                    all_sprites.add(Health_bar)
                    boss = True
                    times += 1
                if boss == True and bosskilled == False:
                    delay += 1
                    if delay == 100:
                        enemybullet_gen()
                        shotgunsound.play()
                        delay = 0        
            if event.type == pygame.MOUSEBUTTONDOWN and pause == False:
                clicked =  True
                
                
            if event.type == pygame.MOUSEBUTTONUP and clicked == True and clip > 0 and pause == False:
                if clip > 0 and not pygame.Rect.colliderect(A.rect, upgrade1.rect) and not  pygame.Rect.colliderect(A.rect, S.rect) and not pygame.Rect.colliderect(A.rect, H.rect) and not pygame.Rect.colliderect(A.rect, moneyup.rect):
                    if shotgun == False:
                        bulletsound.play()
                    if shotgun == True:
                        shotgunsound.play()
                if not pygame.Rect.colliderect(A.rect, pause_b.rect):
                    clip -= 1
                clicked = False
            for coin in coingroup:
                coincollide = pygame.Rect.colliderect(P1.rect, coin.rect)
                if coincollide:
                    moneysound.play()
                    coins_collected += 1 
                    score += 1000 * add_money
                    money += add_money
                    coin.kill()
            for spike in obstacles:
                spike.update()
                death = pygame.Rect.colliderect(P1.rect, spike.rect)
                if death:
                    spike.was_hit = True

            for bird in birdgroup:
                collide = pygame.Rect.colliderect(P1.rect, bird.rect)
                if collide and bird.moving == True:
                    rip.play()
                    birddeath.play()
                    bird.shot()
                    health -= 1
                    score -= 2500
                for bullet in bulletgroup:
                    collide = pygame.Rect.colliderect(bullet.rect, bird.rect)
                    if collide:
                        bird.shot()
                        birddeath.play()
                        bullet.kill()
                        score += 1000
                        birds_shot += 1
            for enemybullet in enemybulletgroup:
                hit_by_bullet = pygame.Rect.colliderect(enemybullet.rect, P1.rect)
                if hit_by_bullet:
                    rip.play()
                    enemybullet.kill()
                    health -= 1
                    score -= 2500
            if boss == True:
                for bullet in bulletgroup:
                    collide = pygame.Rect.colliderect(bullet.rect, M1.rect)
                    if collide and bosskilled == False:
                        rip.play()
                        bullet.kill()
                        bosshealth -= 1
                        Health_bar.update()
                        
            if bosshealth <= 0:
                M1.kill()
          
                mini_bosses_defeated += 1


                bosskilled = True

                    

            
            displaysurface.blit(dg,(0,0))
            spike_gen(h)
            can_gen()
            bird_gen(h)
            cloud_gen(h)
            
            coin_gen()
            ammo_gen()
            
            

            
            if event.type == pygame.MOUSEBUTTONDOWN and pause == False:
                clicked =  True
                
                
                
                
            if event.type == pygame.MOUSEBUTTONUP and clicked == True and clip > 0 and pause == False:

                if not pygame.Rect.colliderect(A.rect, upgrade1.rect) and not  pygame.Rect.colliderect(A.rect, S.rect) and not pygame.Rect.colliderect(A.rect, H.rect) and not pygame.Rect.colliderect(A.rect, moneyup.rect) and not pygame.Rect.colliderect(A.rect, pause_b.rect):
                    
                    if shotgun == False and len(bulletgroup):
                        bulletsound.play()
                    
                    if shotgun == True and len(bulletgroup):
                        shotgunsound.play()
                if not pygame.Rect.colliderect(A.rect, pause_b.rect):       
                    clip -= 1
                clicked = False
            

            h = score/10000
            if pause == False:
                P1.move()
            
            displaysurface.blit(G.surf, G.rect)
            
            displaysurface.blit(upgrade1.surf, upgrade1.rect)
            displaysurface.blit(S.surf, S.rect)
            displaysurface.blit(H.surf, H.rect)
            displaysurface.blit(moneyup.surf, moneyup.rect)
            displaysurface.blit(pause_b.surf, pause_b.rect)
            displaysurface.blit(A.surf, A.rect)
            upgrade1.update()
            S.update()
            H.update()
            moneyup.update()
            
            
            
                        
            n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 25)     
            g  = n.render("Score:" + str(score), True, (0,0,0))   
            displaysurface.blit(g, (30, HEIGHT-50))
            n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 8)     
            m  = n.render("x " + str(clip), True, (0,0,0))   
            displaysurface.blit(m, (30, 60))
            displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"ammo info.png")).convert_alpha(), (30,27)), (0, 50))   
            m  = n.render("x " + str(money), True, (0,0,0))   
            displaysurface.blit(m, (30, 20))
            displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"money_info.png")).convert_alpha(), (30, 30)), (0, 8))
            m  = n.render("x " + str(health), True, (0,0,0))   
            displaysurface.blit(m, (30, 40))
            displaysurface.blit(pygame.transform.scale(pygame.image.load(os.path.join('Images',"health info.png")).convert_alpha(), (80, 40)), (-25, 23))
            m  = n.render("Cost:" + str(cost), True, (0,0,0))   
            displaysurface.blit(m, (WIDTH-90, HEIGHT-70))
            yesshotgun = 0
            if shotgun == True:
                yesshotgun = 9994   
            m  = n.render("Cost:" + str(5 + cost + yesshotgun), True, (0,0,0))   
            displaysurface.blit(m, (WIDTH-165, HEIGHT-70))    
            m  = n.render("Cost:" + str(2 + (cost-1)), True, (0,0,0))   
            displaysurface.blit(m, (WIDTH-232, HEIGHT-70)) 
            m  = n.render("Cost:" + str(1 + cost*2), True, (0,0,0))
            displaysurface.blit(m, (WIDTH-303, HEIGHT-70))
            pygame.display.update()
            FramePerSec.tick(FPS)
            if P1.rect.top > HEIGHT or health <= 0:
                game_done = True
            await asyncio.sleep(0)
        while game_done == True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()
            displaysurface.fill((255,0,0))
            f = n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 40)   
            g  = f.render("Your Score:", True, (0,0,0))   
            displaysurface.blit(g, (WIDTH/2 - 190, HEIGHT/2))
            e = n = pygame.font.Font(os.path.join('Font',"PublicPixel-z84yD.ttf"), 20)   
            if score > hiscore:
                hiscore = score
                    
                with open('score.dat', 'wb') as file:
                    pickle.dump(score, file)
                g  = e.render("New High Score!:" + str(hiscore), True, (0,0,0))
                g_rect = g.get_rect(center=(WIDTH/2, HEIGHT/2 - 250))
                displaysurface.blit(g, g_rect)


            else:
                g  = e.render("High Score: " + str(hiscore), True, (0,0,0))
                g_rect = g.get_rect(center=(WIDTH/2, HEIGHT/2 - 250))
                displaysurface.blit(g, g_rect)


            s = f.render(str(score), True, (0,0,0))
            s_rect = s.get_rect(center=(WIDTH/2, HEIGHT/2 + 110))
            displaysurface.blit(s, s_rect)
            f = font
            p = f.render("[Click] to play again", True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 + 200))
            displaysurface.blit(p, p_rect)
            p = f.render("Coins Collected: " + str(coins_collected), True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 - 200))
            displaysurface.blit(p, p_rect)
            p = f.render("Birds Shot: " + str(birds_shot), True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 - 175))
            displaysurface.blit(p, p_rect)
            p = f.render("Minibosses Defeated: " + str(mini_bosses_defeated), True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 - 150))
            displaysurface.blit(p, p_rect)
            p = f.render("Spikes Hit: " + str(spikes_hit), True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 - 125))
            displaysurface.blit(p, p_rect)
            p = f.render("Times Upgraded: " + str(times_upgraded), True, (0,0,0))
            p_rect = p.get_rect(center=(WIDTH/2, HEIGHT/2 - 100))
            displaysurface.blit(p, p_rect)
            



            pygame.display.update()
            if event.type == pygame.MOUSEBUTTONDOWN:
                score = 0
                game_done = False
                Start = False
            await asyncio.sleep(0)
        HEIGHT = 600
        WIDTH = 880
        ACC = 0.10
        FRIC = -0.12
        FPS = 50
        d= 0
        h = 0
        clip = 8
        money = 0
        cost = 1
        shotgun = False
        clicked = False
        p_clicked = False
        reduction = 0
        pause = False
        health = 5
        game_done = False
        add_money = 1
        Start = False
        high_score = 0
        oldscore = 0
        numbullets = 1
        delay = 0
        bosshealth = 8
        bosskilled = False
        removed_from_pause = False
        score = 0
        numtimes = 1
        times = 1
        t = 0
        move = False
        day = True
        night = False
        st = 0
        orbit = 0
        morning = False
        boss = False
        coins_collected = 0
        birds_shot = 0
        mini_bosses_defeated = 0
        spikes_hit = 0
        times_upgraded = 0

                
        

        FramePerSec.tick(FPS)
        await asyncio.sleep(0)

asyncio.run(main())