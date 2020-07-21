import pygame
import random
import sys
import time

WIDTH = 400
HEIGHT = 600
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Flappy Bird!')
background = [
    pygame.transform.scale(pygame.image.load('img/background-day.png'), (WIDTH, HEIGHT)),
    pygame.transform.scale(pygame.image.load('img/background-night.png'), (WIDTH, HEIGHT))
]

background = background[random.randint(0, 1)].convert()
base = pygame.transform.scale(pygame.image.load('img/base.png'), (WIDTH, 50)).convert()

font = pygame.font.Font('freesansbold.ttf', 32)
font_mini = pygame.font.Font('freesansbold.ttf', 15)
def Menu(menu, start, score):
    WELCOME = font.render('', True, (255, 255, 255))
    GAME_NAME = font.render("Flappy Bird", True, (255, 255, 255))
    AGAIN = font.render("", True, (255, 255, 255))
    score_text = font.render("", True, (255, 255, 255))
    if start:
        WELCOME = font.render('Welcome', True, (255, 255, 255))

    if not start:
        score_text = font.render(f"Your Score: {score}", True, (255, 255, 255))
        AGAIN = font.render("Play Again", True, (255, 255, 255))

    PRESSKEY = font_mini.render("Press any key to start", True, (255, 255, 255))

    while menu:
        pygame.display.flip()
        for events in pygame.event.get():
            if events.type == pygame.QUIT:
                sys.exit()
            if events.type == pygame.KEYDOWN:
                menu = False

        screen.fill((0, 0, 0))
        screen.blit(WELCOME, (125, 100))
        screen.blit(GAME_NAME, (110, 150))
        screen.blit(AGAIN, (105, 300))
        screen.blit(score_text, (100, 200))
        screen.blit(PRESSKEY, (120, 550))


class Bird:
    def __init__(self):
        self.height = HEIGHT // 2
        self.WIDTH = WIDTH // 2 - 100
        self.VEL_UP = -10
        self.VEL_DOWN = 6
        self.transition = 0
        self.score_count = 0
        self.IMAGE = [
            [
                pygame.image.load('img/bluebird-downflap.png').convert_alpha(),
                pygame.image.load('img/bluebird-midflap.png').convert_alpha(),
                pygame.image.load('img/bluebird-upflap.png').convert_alpha()
            ],
            [
                pygame.image.load('img/redbird-downflap.png').convert_alpha(),
                pygame.image.load('img/redbird-midflap.png').convert_alpha(),
                pygame.image.load('img/redbird-upflap.png').convert_alpha()
            ],
            [
                pygame.image.load('img/yellowbird-downflap.png').convert_alpha(),
                pygame.image.load('img/yellowbird-midflap.png').convert_alpha(),
                pygame.image.load('img/yellowbird-upflap.png').convert_alpha()
            ]
        ]
        print(self.IMAGE[0][0])
        self.image_count = 0
        self.img = random.randint(0, 2)

    def move(self):
        self.events = pygame.key.get_pressed()
        self.image_now = self.IMAGE[self.img][self.image_count]
        if self.events[pygame.K_SPACE]:
            self.transition = 0
            self.height += self.VEL_UP
            self.image_now = pygame.transform.rotate(self.image_now, 35)
            if self.image_count < 2:
                self.image_count += 1
            else:
                self.image_count = 0
        elif self.transition >= 5:
            self.height += self.VEL_DOWN
            self.image_now = pygame.transform.rotate(self.image_now, -35)
            self.image_count = 1
        else:
            self.transition += 1
            self.image_now = pygame.transform.rotate(self.image_now, 0)
            if self.image_count < 2:
                self.image_count += 1
            else:
                self.image_count = 0

    def draw(self):
        font = pygame.font.Font('freesansbold.ttf', 22)
        score_text = font.render(f"Score {self.score_count}", False, (0, 0, 0))
        screen.blit(score_text, (WIDTH-100, 50))
        screen.blit(self.image_now, (self.WIDTH, self.height))

    def colide(self, colide):
        if self.height >= 550 or self.height <= 0 or colide:
            Menu(menu, False, self.score_count)
            self.height = HEIGHT // 2
            self.WIDTH = WIDTH // 2 - 100
            self.score_count = 0
            return True
        return False

    def score(self, obs_x):
        if int(obs_x) == self.WIDTH - 5:
            self.score_count += 1


class Pipes:
    def __init__(self):
        self.WIDTH = 52
        self.height = random.randint(100, 400)
        self.HEIGHT = 550
        self.pipe_image = [
            pygame.image.load('img/pipe-green.png').convert_alpha(),
            pygame.image.load('img/pipe-red.png').convert_alpha()
        ]
        self.DISTANCE = 110
        self.game_img = random.randint(0, 1)

        self.x = 400

    def draw(self, vel):

        self.image = pygame.transform.scale(self.pipe_image[self.game_img], (self.WIDTH, self.HEIGHT-self.height+self.DISTANCE))
        self.image_reverse = pygame.transform.scale(pygame.transform.rotate(self.pipe_image[self.game_img], 180), (self.WIDTH, self.HEIGHT-self.height-self.DISTANCE))
        if self.x >= 0:
            self.x -= vel
            screen.blit(self.image, (self.x, self.HEIGHT-self.height))
            screen.blit(self.image_reverse, (self.x, 0))
        else:
            self.x = 400
            self.height = random.randint(100, 400)


    def colide(self, x_bird, y_bird, colide):
        if colide:
            self.x = 400
            self.height = random.randint(100, 400)

        if x_bird == self.x and (y_bird >= self.HEIGHT-self.height-23 or y_bird <= self.HEIGHT-self.height-self.DISTANCE):
            return True
        return False


Obstacule = Pipes()
menu = True
clock = pygame.time.Clock()
bird = Bird()
colide = False
colideobs = False
running = True
Menu(menu, True, 0)
while running:

    screen.blit(background, (0, 0))
    bird.move()
    bird.draw()
    Obstacule.draw(5)
    colide = bird.colide(colideobs)
    colideobs = Obstacule.colide(bird.WIDTH, bird.height, colide)
    screen.blit(base, (0, 550))
    bird.score(Obstacule.x)

    clock.tick(45)

    for events in pygame.event.get():
        if events.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

        if events.type == pygame.KEYDOWN:
            if events.key == pygame.K_ESCAPE:
                Menu(menu, False, score=0)    

    pygame.display.flip()

