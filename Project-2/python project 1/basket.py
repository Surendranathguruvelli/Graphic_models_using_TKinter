import pygame
import random
import sys
from pygame.locals import *
from pygame import gfxdraw
import time

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BALL_RADIUS = 15
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 20
PADDLE_SPEED = 10
BALL_COLORS = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (255, 255, 0), (255, 0, 255)]

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Catch Ball Game")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)

# Load sound effects
catch_sound = pygame.mixer.Sound("514989__toasthatter__ballcatch.wav")
catch_sound.set_volume(0.3)

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((BALL_RADIUS * 2, BALL_RADIUS * 2))
        self.image.set_colorkey((0, 0, 0))
        color = random.choice(BALL_COLORS)
        gfxdraw.filled_circle(self.image, BALL_RADIUS, BALL_RADIUS, BALL_RADIUS - 2, color)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0
        self.speed = 0

    def reset(self, difficulty_level):
        self.speed = random.randint(3, 7) + difficulty_level * 2
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = 0

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > SCREEN_HEIGHT:
            self.reset(1)

class Basket(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((PADDLE_WIDTH, PADDLE_HEIGHT))
        self.image.fill((255, 165, 0))  # Orange color for the basket
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 30
        self.speed = PADDLE_SPEED

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

def get_player_name():
    name = ""
    input_active = True

    while input_active:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_RETURN:
                    input_active = False
                elif event.key == K_BACKSPACE:
                    name = name[:-1]
                else:
                    name += event.unicode

        screen.fill(BLACK)
        name_text = font.render("Enter Your Name: " + name, True, WHITE)
        screen.blit(name_text, (SCREEN_WIDTH // 2 - name_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))
        pygame.display.flip()

    return name

def select_difficulty_level():
    selected_level = 1
    options = ["Easy (30 seconds)", "Medium (1 minute)", "Hard (5 minutes)"]

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                if event.key == K_UP:
                    selected_level = (selected_level - 1) % 3
                elif event.key == K_DOWN:
                    selected_level = (selected_level + 1) % 3
                elif event.key == K_RETURN:
                    return selected_level

        screen.fill(BLACK)
        title_text = font.render("Select Difficulty Level:", True, WHITE)
        screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, SCREEN_HEIGHT // 2 - 60))

        for idx, option in enumerate(options):
            color = WHITE if idx == selected_level else (100, 100, 100)
            option_text = font.render(option, True, color)
            screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, SCREEN_HEIGHT // 2 + idx * 40))

        pygame.display.flip()
        clock.tick(60)

def game_over(player_name, score, total_balls, total_missed):
    restart_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 120, 200, 50)
    menu_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 190, 200, 50)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 + 260, 200, 50)

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if restart_button.collidepoint(mouse_pos):
                    return True
                elif menu_button.collidepoint(mouse_pos):
                    return False
                elif quit_button.collidepoint(mouse_pos):
                    pygame.quit()
                    sys.exit()

        screen.fill(BLACK)
        game_over_text = font.render("Game Over!", True, WHITE)
        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 2 - 100))

        score_text = font.render(f"{player_name}'s Score: {score}", True, WHITE)
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 - 30))

        '''total_balls_text = font.render("Total Balls: {}".format(total_balls), True, WHITE)
        screen.blit(total_balls_text, (SCREEN_WIDTH // 2 - total_balls_text.get_width() // 2, SCREEN_HEIGHT // 2))

        total_missed_text = font.render("Total Missed: {}".format(total_missed), True, WHITE)
        screen.blit(total_missed_text, (SCREEN_WIDTH // 2 - total_missed_text.get_width() // 2, SCREEN_HEIGHT // 2 + 30))'''

        pygame.draw.rect(screen, WHITE, restart_button)
        pygame.draw.rect(screen, WHITE, menu_button)
        pygame.draw.rect(screen, WHITE, quit_button)

        restart_text = font.render("Restart", True, BLACK)
        menu_text = font.render("Menu", True, BLACK)
        quit_text = font.render("Quit", True, BLACK)

        screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2 + 135))
        screen.blit(menu_text, (SCREEN_WIDTH // 2 - menu_text.get_width() // 2, SCREEN_HEIGHT // 2 + 205))
        screen.blit(quit_text, (SCREEN_WIDTH // 2 - quit_text.get_width() // 2, SCREEN_HEIGHT // 2 + 275))

        pygame.display.flip()
        clock.tick(60)

def replay_game(player_name, difficulty_level):
    all_sprites = pygame.sprite.Group()
    balls = pygame.sprite.Group()

    basket = Basket()
    all_sprites.add(basket)

    score = 0
    total_balls = 0
    total_missed = 0
    time_limit = 30 * 1000 if difficulty_level == 0 else (60 if difficulty_level == 1 else 5 * 60) * 1000
    time_remaining = time_limit

    running = True
    last_ball_spawn_time = 0

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

        all_sprites.update()

        # Check collision between ball and basket
        hit_balls = pygame.sprite.spritecollide(basket, balls, True)
        if hit_balls:
            score += len(hit_balls)
            catch_sound.play()

        if time_remaining <= 0:
            # Game over
            if game_over(player_name, score, total_balls, total_missed):
                return True
            else:
                return False

        current_time = pygame.time.get_ticks()
        if current_time - last_ball_spawn_time > 1000:  # Add new ball every second
            last_ball_spawn_time = current_time
            ball = Ball()
            ball.reset(difficulty_level)
            balls.add(ball)
            all_sprites.add(ball)
            total_balls += 1
            total_missed += 1

        screen.fill(BLACK)
        all_sprites.draw(screen)

        # Display score and time remaining
        score_text = font.render("Score: {}".format(score), True, WHITE)
        screen.blit(score_text, (20, 20))

        time_remaining = max(0, time_remaining - clock.get_time())
        time_text = font.render("Time: {:.1f}".format(time_remaining / 1000), True, WHITE)
        screen.blit(time_text, (SCREEN_WIDTH - time_text.get_width() - 20, 20))

        pygame.display.flip()
        clock.tick(60)

def main():
    while True:
        player_name = get_player_name()
        difficulty_level = select_difficulty_level()

        while True:
            if replay_game(player_name, difficulty_level):
                continue
            else:
                break

if __name__ == "__main__":
    main()