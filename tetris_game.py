import pygame
import random

# Настройки
WIDTH, HEIGHT = 300, 600
ROWS, COLS = 20, 10
BLOCK_SIZE = WIDTH // COLS

# Цвета
BLACK = (0, 0, 0)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)
COLORS = [
    (0, 255, 255),  # I
    (0, 0, 255),    # J
    (255, 165, 0),  # L
    (255, 255, 0),  # O
    (0, 255, 0),    # S
    (128, 0, 128),  # T
    (255, 0, 0)     # Z
]

SHAPES = [
    [[1, 1, 1, 1]],
    [[1, 0, 0], [1, 1, 1]],
    [[0, 0, 1], [1, 1, 1]],
    [[1, 1], [1, 1]],
    [[0, 1, 1], [1, 1, 0]],
    [[0, 1, 0], [1, 1, 1]],
    [[1, 1, 0], [0, 1, 1]]
]

pygame.init()
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris with Score and Music")
clock = pygame.time.Clock()

# Музыка
try:
    pygame.mixer.music.load("tetris.mp3")  # Замени на имя своего mp3-файла
    pygame.mixer.music.play(-1)
except:
    print("Музыка не загружена. Пропускаю.")

grid = [[0 for _ in range(COLS)] for _ in range(ROWS)]

font = pygame.font.SysFont("Arial", 20)

score = 0
level = 1
lines_cleared_total = 0

class Piece:
    def __init__(self):
        self.shape = random.choice(SHAPES)
        self.color = random.choice(COLORS)
        self.x = COLS // 2 - len(self.shape[0]) // 2
        self.y = 0

    def rotate(self):
        rotated = [list(row)[::-1] for row in zip(*self.shape)]
        if not self.collision(rotated_shape=rotated):
            self.shape = rotated

    def collision(self, dx=0, dy=0, rotated_shape=None):
        shape = rotated_shape if rotated_shape else self.shape
        for y, row in enumerate(shape):
            for x, cell in enumerate(row):
                if cell:
                    new_x = self.x + x + dx
                    new_y = self.y + y + dy
                    if new_x < 0 or new_x >= COLS or new_y >= ROWS:
                        return True
                    if new_y >= 0 and grid[new_y][new_x]:
                        return True
        return False

    def freeze(self):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell and self.y + y >= 0:
                    grid[self.y + y][self.x + x] = self.color

def draw_grid():
    for y in range(ROWS):
        for x in range(COLS):
            color = grid[y][x] if grid[y][x] else GRAY
            pygame.draw.rect(win, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 0)
            pygame.draw.rect(win, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_piece(piece):
    for y, row in enumerate(piece.shape):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(win, piece.color, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
                pygame.draw.rect(win, BLACK, ((piece.x + x) * BLOCK_SIZE, (piece.y + y) * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    win.blit(score_text, (10, 10))
    win.blit(level_text, (10, 35))

def clear_rows():
    global score, level, lines_cleared_total
    cleared = 0
    new_grid = []
    for row in grid:
        if 0 not in row:
            cleared += 1
        else:
            new_grid.append(row)
    while len(new_grid) < ROWS:
        new_grid.insert(0, [0 for _ in range(COLS)])
    grid[:] = new_grid
    score += cleared * 100
    lines_cleared_total += cleared
    if cleared > 0 and lines_cleared_total // 5 >= level:
        level += 1

def game_over():
    return any(grid[0][x] != 0 for x in range(COLS))

def main():
    global score, level
    run = True
    fall_time = 0
    current_piece = Piece()

    while run:
        win.fill(BLACK)
        draw_grid()
        draw_piece(current_piece)
        draw_score()
        pygame.display.update()

        dt = clock.tick()
        fall_time += dt

        fall_speed = max(100, 500 - (level - 1) * 40)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not current_piece.collision(dx=-1):
                    current_piece.x -= 1
                elif event.key == pygame.K_RIGHT and not current_piece.collision(dx=1):
                    current_piece.x += 1
                elif event.key == pygame.K_DOWN and not current_piece.collision(dy=1):
                    current_piece.y += 1
                elif event.key == pygame.K_UP:
                    current_piece.rotate()

        if fall_time > fall_speed:
            if not current_piece.collision(dy=1):
                current_piece.y += 1
            else:
                current_piece.freeze()
                clear_rows()
                if game_over():
                    print("Game Over. Final Score:", score)
                    run = False
                current_piece = Piece()
            fall_time = 0

    pygame.quit()

if __name__ == "__main__":
    main()
