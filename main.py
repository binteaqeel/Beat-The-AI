import pygame
import random

pygame.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BEAT THE AI")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)

# Load and scale images
human_image = pygame.image.load("human.png").convert_alpha()
ai_image = pygame.image.load("ai.png").convert_alpha()
human2_image = pygame.image.load("human2.png").convert_alpha()
ai2_image = pygame.image.load("ai2.png").convert_alpha()
human_image = pygame.transform.scale(human_image, (human_image.get_width() // 2, human_image.get_height() // 2))
ai_image = pygame.transform.scale(ai_image, (ai_image.get_width() // 2, ai_image.get_height() // 2))
human2_image = pygame.transform.scale(human2_image, (human2_image.get_width() // 2, human2_image.get_height() // 2))
ai2_image = pygame.transform.scale(ai2_image, (ai2_image.get_width() // 2, ai2_image.get_height() // 2))

class Player:
    def __init__(self, x, y, color, image):
        self.rect = pygame.Rect(x, y, image.get_width(), image.get_height())
        self.color = color
        self.image = image
        self.bullets = []
        self.health = 100
        self.state = 'standing'
        self.jump_timer = 0
        self.crouch_timer = 0
        self.can_shoot = True

    def move(self, keys):
        if self.state == 'standing':
            if keys[pygame.K_UP] and self.rect.top > 70:
                self.state = 'jumping'
                self.jump_timer = 20
            elif keys[pygame.K_DOWN] and self.rect.bottom < SCREEN_HEIGHT:
                self.state = 'crouching'
                self.crouch_timer = 20

        if self.state == 'jumping':
            self.rect.y = max(self.rect.y - 10, 70)
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.state = 'standing'

        if self.state == 'crouching':
            if self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += 10
            self.crouch_timer -= 1
            if self.crouch_timer <= 0:
                self.state = 'standing'
            self.rect.y = min(self.rect.y, SCREEN_HEIGHT - self.rect.height)

    def shoot(self):
        bullet_rect = pygame.Rect(self.rect.centerx + 20, self.rect.centery, 10, 5)
        self.bullets.append(bullet_rect)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x += 10
            if bullet.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        for bullet in self.bullets:
            pygame.draw.rect(screen, BLACK, bullet)

class AIPlayer(Player):
    def random_move(self):
        if self.state == 'standing':
            if random.randint(1, 100) <= 50 and self.rect.top > 70:
                self.state = 'jumping'
                self.jump_timer = 20
            elif random.randint(1, 100) > 50 and self.rect.bottom < SCREEN_HEIGHT:
                self.state = 'crouching'
                self.crouch_timer = 20

        if self.state == 'jumping':
            self.rect.y = max(self.rect.y - 10, 70)
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.state = 'standing'

        if self.state == 'crouching':
            if self.rect.bottom < SCREEN_HEIGHT:
                self.rect.y += 10
            self.crouch_timer -= 1
            if self.crouch_timer <= 0:
                self.state = 'standing'
            self.rect.y = min(self.rect.y, SCREEN_HEIGHT - self.rect.height)  # Ensure AI doesn't go below bottom boundary

        if random.randint(1, 100) == 1:
            self.shoot()

    def shoot(self):
        bullet_rect = pygame.Rect(self.rect.centerx - 20, self.rect.centery, 10, 5)  # Center bullet vertically
        self.bullets.append(bullet_rect)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x -= 10
            if bullet.x < 0:
                self.bullets.remove(bullet)

# Initialize players
human_player = Player(150, SCREEN_HEIGHT // 2 - human_image.get_height() // 2, RED, human_image)
ai_player = AIPlayer(SCREEN_WIDTH - 150 - ai_image.get_width(), SCREEN_HEIGHT // 2 - ai_image.get_height() // 2, BLUE, ai_image)

human2_position = None
ai2_position = None
show_human2 = False
show_ai2 = False
show_time = 0
start_ticks = pygame.time.get_ticks()
interval_time = 10000
display_time = 5000
next_show_time = interval_time

def check_bullet_collision(bullets, target):
    for bullet in bullets:
        if target.rect.colliderect(bullet):
            target.health -= 10
            bullets.remove(bullet)

def display_end_screen(winner_text):
    screen.fill(WHITE)
    win_text = font.render(winner_text, True, RED)
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10, 120, 40)
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60, 120, 40)

    pygame.draw.rect(screen, BLUE, play_again_button)
    pygame.draw.rect(screen, RED, quit_button)

    play_again_text = font.render("Play Again", True, WHITE)
    quit_text = font.render("Quit", True, WHITE)

    screen.blit(play_again_text, (play_again_button.x + (play_again_button.width - play_again_text.get_width()) // 2,
                                   play_again_button.y + (play_again_button.height - play_again_text.get_height()) // 2))
    screen.blit(quit_text, (quit_button.x + (quit_button.width - quit_text.get_width()) // 2,
                            quit_button.y + (quit_button.height - quit_text.get_height()) // 2))

    pygame.display.update()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_again_button.collidepoint(event.pos):
                    waiting = False
                    return "play_again"
                elif quit_button.collidepoint(event.pos):
                    pygame.quit()
                    exit()

run = True
while run:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                human_player.shoot()

    current_time = pygame.time.get_ticks()

    if current_time >= next_show_time and not show_human2 and not show_ai2:
        human2_position = (random.randint(0, SCREEN_WIDTH // 2 - human2_image.get_width()),
                           random.randint(0, SCREEN_HEIGHT - human2_image.get_height()))
        ai2_position = (random.randint(SCREEN_WIDTH // 2, SCREEN_WIDTH - ai2_image.get_width()),
                        random.randint(0, SCREEN_HEIGHT - ai2_image.get_height()))
        show_human2 = True
        show_ai2 = True
        next_show_time += interval_time

    if show_human2 and current_time >= next_show_time - display_time:
        show_human2 = False
        show_ai2 = False

    human_player.move(keys)
    ai_player.random_move()

    human_player.update_bullets()
    ai_player.update_bullets()

    check_bullet_collision(human_player.bullets, ai_player)
    check_bullet_collision(ai_player.bullets, human_player)

    if show_ai2 and ai_player.rect.colliderect(pygame.Rect(ai2_position[0], ai2_position[1], ai2_image.get_width(), ai2_image.get_height())):
        ai_player.image = ai_image
        ai_player.health += 10
        ai_player = AIPlayer(ai2_position[0], ai2_position[1], BLUE, ai2_image)
        show_ai2 = False

    if show_human2 and human_player.rect.colliderect(pygame.Rect(human2_position[0], human2_position[1], human2_image.get_width(), human2_image.get_height())):
        human_player.image = human_image
        human_player.health += 10
        human_player = Player(human2_position[0], human2_position[1], RED, human2_image)
        show_human2 = False

    screen.fill(WHITE)

    human_player.draw(screen)
    ai_player.draw(screen)

    if show_human2:
        screen.blit(human2_image, human2_position)
    if show_ai2:
        screen.blit(ai2_image, ai2_position)

    # Display health
    health_text = font.render(f"Health: {human_player.health}", True, BLACK)
    screen.blit(health_text, (10, 10))

    health_text_ai = font.render(f"AI Health: {ai_player.health}", True, BLACK)
    screen.blit(health_text_ai, (SCREEN_WIDTH - health_text_ai.get_width() - 10, 10))

    if human_player.health <= 0:
        display_end_screen("AI Wins!")
        run = False
    if ai_player.health <= 0:
        display_end_screen("Human Wins!")
        run = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
