from pygame import *

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)

back = display.set_mode((700, 500))
display.set_caption('Window')
back.fill(black)

class GameSprite(sprite.Sprite):
    def __init__(self, x, y, width, heinght, picture, speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (width, heinght))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def draw(self):
        back.blit(self.image, self.rect)

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_w] and self.rect.y > 0:
            self.rect.y -= self.speed
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_s] and self.rect.y < 450:
            self.rect.y += self.speed
        if keys[K_d] and self.rect.x < 650:
            self.rect.x += self.speed

    def attack(self):
        pulya = Pulya(self.rect.right, self.rect.centery, 10, 10, 'pulya.png', 15)
        pulya_group.add(pulya)

class Wall(sprite.Sprite):
    def __init__(self, x, y, width, heinght, color):
        super().__init__()
        self.color = color
        self.width = width
        self.height = heinght
        self.image = Surface((self.width, self.height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.image.fill(self.color)

    def draw(self):
        back.blit(self.image, self.rect)

class Enemy(GameSprite):
    derection = 'bot'
    def update(self):
        if self.derection == 'bot':
            self.rect.y += self.speed
        else:
            self.rect.y -= self.speed

        if self.rect.y <= 0:
            self.derection = 'bot'
        if self.rect.y >= 200:
            self.derection = 'top'

class Pulya(GameSprite):
    def update(self):
        self.rect.x += self.speed
        if self.rect.x > 700:
            self.kill()


font.init()
font1 = font.SysFont('Arial', 70)

def text(message, color):
    game_over = font1.render(message, True, white)
    back.fill(color)
    back.blit(game_over, (200, 250))

wall1 = Wall(200, 250, 500, 20, blue)
wall2 = Wall(0, 400, 500, 20, green)
wall3 = Wall(300, 0, 20, 200, red)

wall_group = sprite.Group()
wall_group.add(wall1)
wall_group.add(wall2)
wall_group.add(wall3)

pulya_group = sprite.Group()

player = Player(50, 450, 50, 50, 'player.png', 10)
gold = GameSprite(650, 0, 50, 50, 'cup.png', 0)
enemy = Enemy(500, 50, 50, 50, 'bad.png', 5)

game = True
finish = False
enemy_flag = True

while game:
    for i in event.get():
        if i.type == QUIT:
            game = False
        if i.type == KEYDOWN:
            if i.key == K_SPACE:
                player.attack()

    if finish != True:
        back.fill(black)
        wall_group.draw(back)
        pulya_group.draw(back)
        pulya_group.update()
        player.draw()
        player.update()
        gold.draw()
        if enemy_flag:
            enemy.draw()
            enemy.update()

    if sprite.collide_rect(player, enemy):
        finish = True
        text('Game Over!', red)

    if sprite.collide_rect(player, gold):
        finish = True
        text('You Win!', green)

    if sprite.spritecollide(player, wall_group, True):
        finish = True
        text('Game Over!', red)

    if sprite.spritecollide(enemy, pulya_group, True):
        enemy_flag = False
        enemy.rect.x = 1000
        enemy.rect.y = 1000


    display.update()
    time.delay(50)
