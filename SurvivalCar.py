import pygame
import random
pygame.init()

width = 800
height = 600

center = width//2

black = (0, 0, 0)
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 255, 0)
light_blue = (135, 206, 235)
blue = (0, 0, 255)
purple = (138, 43, 226)

colors = [red, orange, yellow, green, light_blue, blue, purple]
car_color = random.choice(colors)

def flip_through_colors(color):
        return color

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Dangerous Highway")

class player_car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_width, car_height):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.image.fill(red)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.player_speed = 5
    def update(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rect.x -= self.player_speed
        if keys[pygame.K_d]:
            self.rect.x += self.player_speed

class enemy_car(pygame.sprite.Sprite):
    def __init__(self, x, y, car_width, car_height):
        super().__init__()
        self.image = pygame.Surface((car_width, car_height))
        self.color = random.choice(colors)
        self.image.fill(self.color)
        self.rect = self.image.get_rect(bottomleft=(x, y))
        self.velocity_y = 0
        self.gravity = .5
    def update(self):
        if self.rect.top > height:
            self.respawn()
            

        self.velocity_y += self.gravity
        self.rect.y += self.velocity_y
    def respawn(self):
        self.rect.x = random.randint(0, width - self.rect.width)
        self.rect.y = 0
        self.velocity_y = 0
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.rect.x, self.rect.y, self.rect.width, self.rect.width))


        
        

player = player_car(x=center, y=height, car_width=70, car_height=100)
player_group = pygame.sprite.Group(player)

enemy = enemy_car(x= random.randint(0, width), y=0, car_width=70, car_height=100)
enemy_group = pygame.sprite.Group(enemy)

running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    hit = pygame.sprite.spritecollide(player, enemy_group, False)
    if hit:
        pygame.quit()
    player_group.update()
    enemy_group.update()

    screen.fill(black)

    player_group.draw(screen)
    enemy_group.draw(screen, random.choice(colors))
    pygame.display.flip()
    clock.tick(60)
pygame.quit()