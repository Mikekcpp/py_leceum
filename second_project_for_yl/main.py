import pygame
import sys
import random

pygame.init()

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 600
FPS = 20
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
ADD_NEW_FLAME_RATE = 25

cactus_img = pygame.image.load("data/cactus_bricks.png")
fire_img = pygame.image.load("data/fire_bricks.png")
cactus_img_rect = cactus_img.get_rect()
cactus_img_rect.left = 0
fire_img_rect = fire_img.get_rect()
fire_img_rect.left = 0
CLOCK = pygame.time.Clock()
font = pygame.font.SysFont("forte", 20)

canvas = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Mario")

selected_character = None


class Topscore:
    def __init__(self):
        self.high_score = 0

    def top_score(self, score):
        if score > self.high_score:
            self.high_score = score
        return self.high_score


topscore = Topscore()


class Dragon:
    dragon_velocity = 10

    def __init__(self):
        self.dragon_img = pygame.image.load("data/dragon.png")
        self.dragon_img_rect = self.dragon_img.get_rect()
        self.dragon_img_rect.width -= 10
        self.dragon_img_rect.height -= 10
        self.dragon_img_rect.top = WINDOW_HEIGHT / 2
        self.dragon_img_rect.right = WINDOW_WIDTH
        self.up = True
        self.down = False

    def update(self):
        canvas.blit(self.dragon_img, self.dragon_img_rect)
        if self.dragon_img_rect.top <= cactus_img_rect.bottom:
            self.up = False
            self.down = True
        elif self.dragon_img_rect.bottom >= fire_img_rect.top:
            self.up = True
            self.down = False

        if self.up:
            self.dragon_img_rect.top -= self.dragon_velocity
        elif self.down:
            self.dragon_img_rect.top += self.dragon_velocity


class Flames:
    flames_velocity = 20

    def __init__(self):
        self.flames = pygame.image.load("data/fireball.png")
        self.flames_img = pygame.transform.scale(self.flames, (20, 20))
        self.flames_img_rect = self.flames_img.get_rect()
        self.flames_img_rect.right = dragon.dragon_img_rect.left
        self.flames_img_rect.top = dragon.dragon_img_rect.top + 30

    def update(self):
        canvas.blit(self.flames_img, self.flames_img_rect)

        if self.flames_img_rect.left > 0:
            self.flames_img_rect.left -= self.flames_velocity


class Mario:
    velocity = 10

    def __init__(self):
        self.image = pygame.image.load("data\mario.gif")
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = WINDOW_HEIGHT / 2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.image, self.rect)
        if self.rect.top <= cactus_img_rect.bottom:
            game_over()
        if self.rect.bottom >= fire_img_rect.top:
            game_over()
        if self.up:
            self.rect.top -= 10
        if self.down:
            self.rect.bottom += 10


class Luigi:
    velocity = 10

    def __init__(self):
        self.image = pygame.image.load("data/luigi.gif")
        self.rect = self.image.get_rect()
        self.rect.left = 20
        self.rect.top = WINDOW_HEIGHT / 2 - 100
        self.down = True
        self.up = False

    def update(self):
        canvas.blit(self.image, self.rect)
        if self.rect.top <= cactus_img_rect.bottom:
            game_over()
        if self.rect.bottom >= fire_img_rect.top:
            game_over()
        if self.up:
            self.rect.top -= 10
        if self.down:
            self.rect.bottom += 10


class Bonus:
    def __init__(self):
        self.image = pygame.image.load("data/bonus.png")
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(WINDOW_WIDTH, WINDOW_WIDTH + 100)
        self.rect.y = random.randint(50, WINDOW_HEIGHT - 50)

    def update(self):
        self.rect.x -= 5
        canvas.blit(self.image, self.rect)


def character_selection():
    global selected_character
    while True:
        canvas.fill(BLACK)
        title_font = font.render("Выберите персонажа:", True, GREEN)
        title_rect = title_font.get_rect(center=(WINDOW_WIDTH / 2, 100))
        canvas.blit(title_font, title_rect)

        mario_img = pygame.image.load("data\mario.gif")
        luigi_img = pygame.image.load("data\luigi.gif")

        canvas.blit(mario_img, (WINDOW_WIDTH / 2 - 100, 200))
        canvas.blit(luigi_img, (WINDOW_WIDTH / 2 + 50, 200))

        instructions_font = font.render(
            'Нажмите "M" для Марио или "L" для Луиджи', True, GREEN
        )
        instructions_rect = instructions_font.get_rect(center=(WINDOW_WIDTH / 2, 400))
        canvas.blit(instructions_font, instructions_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    selected_character = "mario"
                    return
                elif event.key == pygame.K_l:
                    selected_character = "luigi"
                    return

        pygame.display.update()


def check_level(SCORE):
    global LEVEL
    if SCORE in range(0, 10):
        cactus_img_rect.bottom = 50
        fire_img_rect.top = WINDOW_HEIGHT - 50
        LEVEL = 1
    elif SCORE in range(10, 20):
        cactus_img_rect.bottom = 100
        fire_img_rect.top = WINDOW_HEIGHT - 100
        LEVEL = 2
    elif SCORE in range(20, 30):
        cactus_img_rect.bottom = 150
        fire_img_rect.top = WINDOW_HEIGHT - 150
        LEVEL = 3
    elif SCORE > 30:
        cactus_img_rect.bottom = 200
        fire_img_rect.top = WINDOW_HEIGHT - 200
        LEVEL = 4


def surprise_effect():
    surprise_img = pygame.image.load("data/бу.webp")
    surprise_img_rect = surprise_img.get_rect()
    surprise_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)

    start_ticks = pygame.time.get_ticks()
    while True:
        canvas.fill(BLACK)
        canvas.blit(surprise_img, surprise_img_rect)
        pygame.display.update()

        if pygame.time.get_ticks() - start_ticks > 2000:
            break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def start_game():
    canvas.fill(BLACK)
    start_img = pygame.image.load("data/start.png")
    start_img_rect = start_img.get_rect()
    start_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(start_img, start_img_rect)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                game_loop()
        pygame.display.update()


def game_loop():
    character_selection()

    global dragon
    global SCORE
    global HIGH_SCORE

    # lives = 3
    SCORE = 0
    flames_list = []
    bonus_list = []
    bonus_timer = 0

    while True:
        dragon = Dragon()
        flames = Flames()

        if selected_character == "mario":
            mario = Mario()
            luigi = None
        elif selected_character == "luigi":
            mario = Luigi()
            luigi = Luigi()

        add_new_flame_counter = 0
        SCORE = 0
        flames_list = []
        pygame.mixer.music.load("data/mario_theme.wav")
        pygame.mixer.music.play(-1, 0.0)

        surprise_time = random.randint(5000, 15000)
        last_surprise_time = pygame.time.get_ticks()

        while True:
            canvas.fill(BLACK)
            check_level(SCORE)
            dragon.update()
            add_new_flame_counter += 1

            bonus_timer += 1
            if bonus_timer > 100:
                bonus = Bonus()
                bonus_list.append(bonus)
                bonus_timer = 0

            for bonus in bonus_list:
                bonus.update()
                if bonus.rect.colliderect(mario.rect):
                    SCORE += 5
                    bonus_list.remove(bonus)

            if add_new_flame_counter == ADD_NEW_FLAME_RATE:
                add_new_flame_counter = 0
                new_flame = Flames()
                flames_list.append(new_flame)
            for f in flames_list:
                if f.flames_img_rect.left <= 0:
                    flames_list.remove(f)
                    SCORE += 1

                # if f.flames_img_rect.colliderect(mario.rect):
                #     lives -= 1
                #     flames_list.remove(f)
                #     if lives <= 0:
                #         game_over()
                f.update()

            current_time = pygame.time.get_ticks()
            if current_time - last_surprise_time > surprise_time:
                surprise_effect()
                last_surprise_time = current_time
                surprise_time = random.randint(5000, 15000)

            if LEVEL > 2:
                if luigi is None:
                    luigi = Luigi()

                luigi.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        mario.up = True
                        mario.down = False
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        mario.up = False
                        mario.down = True
                    elif event.key == pygame.K_DOWN:
                        mario.down = True
                        mario.up = False

            score_font = font.render("Score:" + str(SCORE), True, GREEN)
            score_font_rect = score_font.get_rect()
            score_font_rect.center = (
                300,
                cactus_img_rect.bottom + score_font_rect.height / 2,
            )
            canvas.blit(score_font, score_font_rect)

            level_font = font.render("Level:" + str(LEVEL), True, GREEN)
            level_font_rect = level_font.get_rect()
            level_font_rect.center = (
                500,
                cactus_img_rect.bottom + score_font_rect.height / 2,
            )
            canvas.blit(level_font, level_font_rect)

            top_score_font = font.render(
                "Top Score:" + str(topscore.high_score), True, GREEN
            )
            top_score_font_rect = top_score_font.get_rect()
            top_score_font_rect.center = (
                700,
                cactus_img_rect.bottom + score_font_rect.height / 2,
            )
            canvas.blit(top_score_font, top_score_font_rect)

            # lives_font = font.render("Lives: " + str(lives), True, GREEN)
            # lives_font_rect = lives_font.get_rect()
            # lives_font_rect.center = (
            #     800,
            #     cactus_img_rect.bottom + score_font_rect.height / 2,
            # )
            # canvas.blit(lives_font, lives_font_rect)

            canvas.blit(cactus_img, cactus_img_rect)
            canvas.blit(fire_img, fire_img_rect)
            mario.update()
            for f in flames_list:
                if f.flames_img_rect.colliderect(mario.rect):
                    game_over()
                    if SCORE > mario.mario_score:
                        mario.mario_score = SCORE
            pygame.display.update()
            CLOCK.tick(FPS)


def game_over():
    pygame.mixer.music.stop()
    music = pygame.mixer.Sound("data/mario_dies.wav")
    music.play()
    topscore.top_score(SCORE)
    game_over_img = pygame.image.load("data/end.png")
    game_over_img_rect = game_over_img.get_rect()
    game_over_img_rect.center = (WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
    canvas.blit(game_over_img, game_over_img_rect)

    # lives_font = font.render("Lives: 0", True, GREEN)
    # lives_font_rect = lives_font.get_rect(
    #     center=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 50)
    # )
    # canvas.blit(lives_font, lives_font_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                music.stop()
                game_loop()
        pygame.display.update()


start_game()
