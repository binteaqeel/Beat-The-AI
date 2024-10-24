import pygame
import random

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("BEAT THE AI")

clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

font = pygame.font.Font(None, 36)


class Player:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x, y, 50, 200)
        self.color = color
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

            elif keys[pygame.K_DOWN]:
                if self.rect.bottom + 10 <= SCREEN_HEIGHT:
                    self.state = 'crouching'
                    self.crouch_timer = 20

        if self.state == 'jumping':
            self.rect.y -= 10
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.state = 'standing'
                self.rect.y += 10

        if self.state == 'crouching':
            if self.rect.bottom + 10 <= SCREEN_HEIGHT:
                self.rect.y += 10
            self.crouch_timer -= 1
            if self.crouch_timer <= 0:
                self.state = 'standing'
                self.rect.y -= 10

    def shoot(self):
        bullet_rect = pygame.Rect(self.rect.centerx + 20, self.rect.centery + 90, 10, 5)
        self.bullets.append(bullet_rect)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x += 10
            if bullet.x > SCREEN_WIDTH:
                self.bullets.remove(bullet)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

        # Draw bullets
        for bullet in self.bullets:
            pygame.draw.rect(screen, BLACK, bullet)


class AIPlayer(Player):
    def __init__(self, x, y, color):
        super().__init__(x, y, color)

    def random_move(self):
        if self.state == 'standing':
            if random.randint(1, 100) <= 50:
                if self.rect.top > 70:
                    self.state = 'jumping'
                    self.jump_timer = 20
            elif random.randint(1, 100) > 50:
                if self.rect.bottom < SCREEN_HEIGHT:
                    self.state = 'crouching'
                    self.crouch_timer = 20

        if self.state == 'jumping':
            self.rect.y -= 10
            self.jump_timer -= 1
            if self.jump_timer <= 0:
                self.state = 'standing'
                self.rect.y += 10

        if self.state == 'crouching':
            if self.rect.bottom + 10 <= SCREEN_HEIGHT:
                self.rect.y += 10
            self.crouch_timer -= 1
            if self.crouch_timer <= 0:
                self.state = 'standing'
                self.rect.y -= 10

        if random.randint(1, 100) == 1:
            self.shoot()

    def shoot(self):
        bullet_rect = pygame.Rect(self.rect.centerx - 20, self.rect.centery + 90, 10, 5)
        self.bullets.append(bullet_rect)

    def update_bullets(self):
        for bullet in self.bullets:
            bullet.x -= 10
            if bullet.x < 0:
                self.bullets.remove(bullet)


human_player = Player(200, SCREEN_HEIGHT // 2 - 100, RED)
ai_player = AIPlayer(600, SCREEN_HEIGHT // 2 - 100, BLUE)

def check_bullet_collision(bullets, target):
    for bullet in bullets:
        if target.rect.colliderect(bullet):
            if (target.state == 'standing' and human_player.state == 'standing') or \
                    (target.state == 'jumping' and human_player.state == 'jumping') or \
                    (target.state == 'crouching' and human_player.state == 'crouching'):
                target.health -= 10
                bullets.remove(bullet)


def display_end_screen(winner_text):
    screen.fill(WHITE)
    win_text = font.render(winner_text, True, RED)
    screen.blit(win_text, (SCREEN_WIDTH // 2 - win_text.get_width() // 2, SCREEN_HEIGHT // 2 - 50))

    play_again_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 10, 120, 40)  # Increased size
    quit_button = pygame.Rect(SCREEN_WIDTH // 2 - 120, SCREEN_HEIGHT // 2 + 60, 120, 40)  # Increased size

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

    human_player.move(keys)

    ai_player.random_move()

    human_player.update_bullets()
    ai_player.update_bullets()

    check_bullet_collision(human_player.bullets, ai_player)
    check_bullet_collision(ai_player.bullets, human_player)

    screen.fill(WHITE)
    human_player.draw(screen)
    ai_player.draw(screen)

    pygame.draw.rect(screen, RED, (20, 20, human_player.health * 2, 20))
    pygame.draw.rect(screen, BLUE, (SCREEN_WIDTH - 220, 20, ai_player.health * 2, 20))

    if human_player.health <= 0:
        winner = "AI WINS!"
        result = display_end_screen(winner)
        if result == "play_again":
            human_player.health = 100
            ai_player.health = 100
    elif ai_player.health <= 0:
        winner = "HUMAN WINS"
        result = display_end_screen(winner)
        if result == "play_again":
            human_player.health = 100
            ai_player.health = 100

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
