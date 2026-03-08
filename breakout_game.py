# Breakout Full Version with Sounds, Bonuses, Lives, Multi-hit Bricks
import pygame
import random

# --- Constants ---
WIDTH, HEIGHT = 600, 800
FPS = 60
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 15
BALL_RADIUS = 10
BRICK_WIDTH = 60
BRICK_HEIGHT = 25
ROWS, COLS = 6, 10
LIVES = 3

# --- Colors ---
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)
COLORS = [(255, 100, 100), (255, 200, 0), (0, 200, 255), (0, 255, 0)]

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Breakout Deluxe")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

# --- Sounds ---
try:
    # bounce_sound = pygame.mixer.Sound("tetris1.mp3")
    break_sound = pygame.mixer.Sound("drop.wav")
    powerup_sound = pygame.mixer.Sound("clear.wav")
except:
    # bounce_sound = 
    break_sound = powerup_sound = None
    print("Some sounds missing")

# --- Classes ---
class Paddle:
    def __init__(self):
        self.width = PADDLE_WIDTH
        self.rect = pygame.Rect(WIDTH // 2 - self.width // 2, HEIGHT - 40, self.width, PADDLE_HEIGHT)
        self.speed = 8

    def move(self, dx):
        self.rect.x += dx * self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))

    def draw(self):
        pygame.draw.rect(win, WHITE, self.rect)

class Ball:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.dx = random.choice([-4, 4])
        self.dy = -4
        self.radius = BALL_RADIUS

    def move(self):
        self.x += self.dx
        self.y += self.dy

        if self.x <= 0 or self.x >= WIDTH:
            self.dx *= -1
            # if bounce_sound: bounce_sound.play()
        if self.y <= 0:
            self.dy *= -1
            # if bounce_sound: bounce_sound.play()

    def draw(self):
        pygame.draw.circle(win, WHITE, (int(self.x), int(self.y)), self.radius)

    def collide_with_paddle(self, paddle):
        if paddle.rect.collidepoint(self.x, self.y + self.radius):
            self.dy *= -1
            offset = (self.x - paddle.rect.centerx) / (paddle.rect.width / 2)
            self.dx = offset * 5
            # if bounce_sound: bounce_sound.play()

    def collide_with_brick(self, brick):
        if brick.rect.collidepoint(self.x, self.y):
            self.dy *= -1
            return True
        return False

class Brick:
    def __init__(self, x, y, hits=1):
        self.rect = pygame.Rect(x, y, BRICK_WIDTH, BRICK_HEIGHT)
        self.hits = hits

    def draw(self):
        color = COLORS[min(self.hits - 1, len(COLORS) - 1)]
        pygame.draw.rect(win, color, self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 2)

class PowerUp:
    def __init__(self, x, y, effect):
        self.rect = pygame.Rect(x, y, 20, 20)
        self.effect = effect
        self.dy = 3

    def update(self):
        self.rect.y += self.dy

    def draw(self):
        pygame.draw.rect(win, (200, 255, 0), self.rect)
        pygame.draw.rect(win, BLACK, self.rect, 1)

# --- Game Logic ---
def create_bricks():
    bricks = []
    for row in range(ROWS):
        for col in range(COLS):
            x = col * (BRICK_WIDTH + 5) + 35
            y = row * (BRICK_HEIGHT + 5) + 60
            hits = random.choice([1, 1, 2])
            bricks.append(Brick(x, y, hits))
    return bricks

def draw_ui(score, lives):
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    win.blit(score_text, (20, 10))
    win.blit(lives_text, (WIDTH - 100, 10))

def main():
    paddle = Paddle()
    ball = Ball()
    bricks = create_bricks()
    powerups = []
    score = 0
    lives = LIVES
    run = True

    while run:
        clock.tick(FPS)
        win.fill(BLACK)

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            paddle.move(-1)
        if keys[pygame.K_RIGHT]:
            paddle.move(1)

        # Move ball
        ball.move()
        ball.collide_with_paddle(paddle)

        # Ball falls
        if ball.y > HEIGHT:
            lives -= 1
            ball.reset()
            if lives == 0:
                run = False

        # Brick collisions
        for brick in bricks[:]:
            if ball.collide_with_brick(brick):
                brick.hits -= 1
                if break_sound: break_sound.play()
                if brick.hits <= 0:
                    bricks.remove(brick)
                    score += 100
                    if random.random() < 0.2:
                        powerups.append(PowerUp(brick.rect.x + 20, brick.rect.y, "expand"))
                break

        # PowerUps
        for powerup in powerups[:]:
            powerup.update()
            powerup.draw()
            if powerup.rect.colliderect(paddle.rect):
                if powerup.effect == "expand":
                    paddle.width += 40
                    paddle.rect.width = paddle.width
                    if powerup_sound: powerup_sound.play()
                powerups.remove(powerup)

        # Draw
        paddle.draw()
        ball.draw()
        for brick in bricks:
            brick.draw()
        draw_ui(score, lives)

        pygame.display.flip()

        if not bricks:
            run = False

    pygame.time.delay(1500)
    pygame.quit()

if __name__ == "__main__":
    main()