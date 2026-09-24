import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH = 800
HEIGHT = 600
CELL_SIZE = 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Colors
BLACK = (20, 20, 20)
GREEN = (0, 200, 80)
DARK_GREEN = (0, 140, 60)
RED = (220, 50, 50)
WHITE = (255, 255, 255)
GRAY = (150, 150, 150)

# Fonts
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 70)

clock = pygame.time.Clock()


def random_food():
    x = random.randrange(0, WIDTH, CELL_SIZE)
    y = random.randrange(0, HEIGHT, CELL_SIZE)
    return [x, y]


def draw_snake(snake):
    for i, segment in enumerate(snake):
        color = GREEN if i == 0 else DARK_GREEN
        pygame.draw.rect(
            screen,
            color,
            (segment[0], segment[1], CELL_SIZE, CELL_SIZE)
        )


def draw_food(food):
    pygame.draw.rect(
        screen,
        RED,
        (food[0], food[1], CELL_SIZE, CELL_SIZE)
    )


def show_score(score):
    text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(text, (10, 10))


def game_over(score):
    screen.fill(BLACK)

    title = big_font.render("GAME OVER", True, RED)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    restart_text = font.render(
        "Press R to Restart or Q to Quit",
        True,
        GRAY
    )

    screen.blit(
        title,
        (WIDTH // 2 - title.get_width() // 2, 200)
    )

    screen.blit(
        score_text,
        (WIDTH // 2 - score_text.get_width() // 2, 290)
    )

    screen.blit(
        restart_text,
        (WIDTH // 2 - restart_text.get_width() // 2, 350)
    )

    pygame.display.update()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return

                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()


def main():
    snake = [
        [400, 300],
        [380, 300],
        [360, 300]
    ]

    direction = [CELL_SIZE, 0]
    next_direction = direction.copy()

    food = random_food()
    score = 0
    speed = 10

    running = True

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_UP and direction != [0, CELL_SIZE]:
                    next_direction = [0, -CELL_SIZE]

                elif event.key == pygame.K_DOWN and direction != [0, -CELL_SIZE]:
                    next_direction = [0, CELL_SIZE]

                elif event.key == pygame.K_LEFT and direction != [CELL_SIZE, 0]:
                    next_direction = [-CELL_SIZE, 0]

                elif event.key == pygame.K_RIGHT and direction != [-CELL_SIZE, 0]:
                    next_direction = [CELL_SIZE, 0]

        direction = next_direction.copy()

        # Move snake
        new_head = [
            snake[0][0] + direction[0],
            snake[0][1] + direction[1]
        ]

        # Wall collision
        if (
            new_head[0] < 0
            or new_head[0] >= WIDTH
            or new_head[1] < 0
            or new_head[1] >= HEIGHT
        ):
            game_over(score)
            return

        # Self collision
        if new_head in snake:
            game_over(score)
            return

        snake.insert(0, new_head)

        # Food collision
        if new_head == food:
            score += 1
            food = random_food()

            # Increase speed gradually
            if score % 5 == 0:
                speed += 1
        else:
            snake.pop()

        # Draw everything
        screen.fill(BLACK)

        draw_snake(snake)
        draw_food(food)
        show_score(score)

        pygame.display.update()

        clock.tick(speed)


def start_game():
    while True:
        main()


start_game()