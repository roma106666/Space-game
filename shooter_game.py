import pygame
from random import randint

pygame.init()
pygame.time.set_timer(pygame.USEREVENT,1000)

pygame.mixer.music.load('music.mp3')
pygame.mixer.music.play(-1)

b_s = pygame.mixer.Sound('bullet_sound.ogg')
stl = pygame.mixer.Sound('stl_meteor.ogg')

w = 1200
h = 800
fps = 144

WHITE = (255,255,255)
BLUE = (51, 204, 255)

print_label = pygame.font.SysFont('comicsansms',70)

r = ['ufo.png','meteor2.png','asteroid.png']

mw = pygame.display.set_mode((w,h))
space = pygame.image.load('fon.jpg').convert()
pygame.display.set_caption('Game')
back = pygame.transform.scale(space, (w,h))

clock = pygame.time.Clock()

class Hero(pygame.sprite.Sprite):
    def __init__(self, picture, speed, x, y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load(picture), (150,150)).convert_alpha()
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.x = x
        self.rect.y = y

    def fire(self):
        bullet = Bullet('pula1.png', 10, self.rect.centerx - 10, self.rect.top)
        bullets.add(bullet)

class Bullet(Hero):
    def __init__(self,picture ,speed,x,y):
        super().__init__(picture,speed,x,y)
        self.image = pygame.transform.scale(pygame.image.load(picture), (20,20)).convert_alpha()

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y > h:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self,picture,speed,x,group):
        super().__init__()
        self.image = picture
        self.rect = self.image.get_rect(center=(x,0))
        self.speed = speed
        self.add(group)

    def update(self):
        global xp
        global win
        if self.rect.y < h:
            self.rect.y += self.speed
        else:
            self.kill()
            create_enemy(enemies,r[randint(0,len(r)-1)])
            xp -= 1

def create_enemy(group,picture):
    enemy_image = pygame.transform.scale(pygame.image.load(picture), (50,50)).convert_alpha() 
    x = randint(20, w - 20)
    speed = randint(1,3)
    return Enemy(enemy_image,speed,x,group)

def stats():
    global xp
    global win
    global game_score
    for enemy in enemies:
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                game_score += 1
    for enemy in enemies2 :
        for bullet in bullets:
            if enemy.rect.colliderect(bullet.rect):
                game_score += 1
    for enemy in enemies2:
        if space_ship.rect.colliderect(enemy.rect):
            enemy.kill()
            xp -= 1
            stl.play()
    for enemy in enemies:
        if space_ship.rect.colliderect(enemy.rect):
            enemy.kill()
            xp -=1
            stl.play()

def pause():
    paused = True
    while paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()

        score_text = print_label.render(str(game_score), True, WHITE)
        mw.blit(score_text, (0, 0))

        text = print_label.render('Paused. Press enter to continue',True,WHITE)
        mw.blit(text,(w//2-400,h//2))

        keys = pygame.key.get_pressed()
        if keys[pygame.K_RETURN]:
            paused = False

        pygame.display.update()
        clock.tick(fps)


space_ship = Hero('ship.png', 5, w // 2-60, h - 150)
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
enemies2 = pygame.sprite.Group()
create_enemy(enemies,r[randint(0,len(r)-1)])

win = True

game_score = 0

xp = 3

win_score = randint(50,80)

while True:
    stats()
    mw.blit(back, (0, 0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
        elif event.type == pygame.USEREVENT:
            create_enemy(enemies,r[randint(0,len(r)-1)])
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                space_ship.fire()
                b_s.play()

    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        space_ship.rect.x -= space_ship.speed
    if keys[pygame.K_d]:
        space_ship.rect.x += space_ship.speed
    if keys[pygame.K_s]:
        space_ship.rect.y += space_ship.speed
    if keys[pygame.K_w]:
        space_ship.rect.y -= space_ship.speed
    if keys[pygame.K_ESCAPE]:
        pause()

    if game_score == 15:
        space_ship = Hero('corabl2.png', 7, space_ship.rect.x,space_ship.rect.y)
    if game_score == 35:
        space_ship = Hero('ship3.png', 10, space_ship.rect.x,space_ship.rect.y)

    score_text = print_label.render('Счёт:' + str(game_score), True, WHITE)
    mw.blit(score_text,(0,0))

    xp_text = print_label.render('XP:' + str(xp), True, WHITE)
    mw.blit(xp_text,(0,50))

    if xp == 0:
        win = False

    bullets.draw(mw)
    enemies.draw(mw)

    mw.blit(space_ship.image, space_ship.rect)

    clock.tick(fps)

    pygame.sprite.groupcollide(enemies,bullets, True,True)
    pygame.sprite.groupcollide(enemies2, bullets, True,True)

    bullets.update()
    enemies.update()

    if not win:
        mw.blit(pygame.transform.scale(pygame.image.load('lose.png'), (w,h)),(0,0))
        pygame.mixer.music.stop()
    if game_score == win_score:
        mw.blit(pygame.transform.scale(pygame.image.load('win.png'), (w,h)),(0,0))
        pygame.mixer.music.stop()

    pygame.display.update()