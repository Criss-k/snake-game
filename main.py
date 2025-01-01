import pygame
import random
import sys

# Initialize pygame
pygame.init()

# Constants for the game
WIDTH, HEIGHT = 800, 600  # Screen dimensions
BLOCK_SIZE = 20  # Size of each block (snake segment and food)
FPS = 10  # Frames per second (controls game speed)
BORDER_THICKNESS = BLOCK_SIZE  # Thickness of the border

# Colors
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
GLASS = (173, 216, 230, 128)  # Light blue with some transparency
SUPER_SNACK_COLOR = (255, 223, 0)  # Gold color
SNALE_SNACK_COLOR = (138, 43, 226)  # Blue-violet color
SPEED_SNACK_COLOR = (0, 255, 255)  # Cyan color

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

# Initialize fonts
font = pygame.font.Font(None, 36)

def draw_border():
    # Draw top border
    pygame.draw.rect(screen, GLASS, (0, 0, WIDTH, BORDER_THICKNESS))
    # Draw bottom border
    pygame.draw.rect(screen, GLASS, (0, HEIGHT - BORDER_THICKNESS, WIDTH, BORDER_THICKNESS))
    # Draw left border
    pygame.draw.rect(screen, GLASS, (0, 0, BORDER_THICKNESS, HEIGHT))
    # Draw right border
    pygame.draw.rect(screen, GLASS, (WIDTH - BORDER_THICKNESS, 0, BORDER_THICKNESS, HEIGHT))

# Draw snake
def draw_snake(snake):
    for segment in snake:
        pygame.draw.rect(screen, GREEN, (*segment, BLOCK_SIZE, BLOCK_SIZE))

# Move snake
def move_snake(snake, direction):
    head = snake[0]
    if direction == "UP":
        new_head = (head[0], head[1] - BLOCK_SIZE)
    elif direction == "DOWN":
        new_head = (head[0], head[1] + BLOCK_SIZE)
    elif direction == "LEFT":
        new_head = (head[0] - BLOCK_SIZE, head[1])
    elif direction == "RIGHT":
        new_head = (head[0] + BLOCK_SIZE, head[1])
    else:
        new_head = head  # No movement if no valid direction
    snake.insert(0, new_head)  # Add new head
    snake.pop()  # Remove tail

# Draw food
def draw_food(food, color):
    pygame.draw.rect(screen, color, (*food, BLOCK_SIZE, BLOCK_SIZE))

# Check for food collision
def check_food_collision(snake, food):
    if snake[0] == food:  # If head is on the food
        return True
    return False

# Generate random food position
def generate_food(snake):
    while True:
        x = random.randint(BORDER_THICKNESS // BLOCK_SIZE, (WIDTH // BLOCK_SIZE) - 2) * BLOCK_SIZE
        y = random.randint(BORDER_THICKNESS // BLOCK_SIZE, (HEIGHT // BLOCK_SIZE) - 2) * BLOCK_SIZE
        if (x, y) not in snake:  # Ensure food is not generated on the snake
            return x, y

# Check for collisions
def check_collision(snake):
    head = snake[0]
    # Check wall collision
    if head[0] < BORDER_THICKNESS or head[1] < BORDER_THICKNESS or head[0] >= WIDTH - BORDER_THICKNESS or head[1] >= HEIGHT - BORDER_THICKNESS:
        return True
    # Check self collision
    if head in snake[1:]:
        return True
    return False

# Draw score
def draw_score(score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

# Display Game Over screen
def game_over_screen(score):
    screen.fill(BLACK)
    game_over_text = font.render("Game Over!", True, WHITE)
    restart_text = font.render("Press 'R' to Restart or 'Q' to Quit.", True, WHITE)
    score_text = font.render(f"Final Score: {score}", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
    screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 50))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2))
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Restart the game
                    return True
                elif event.key == pygame.K_q:  # Quit the game
                    pygame.quit()
                    sys.exit()

# Main game function
def main():
    # Game variables
    snake = [(100, 100), (80, 100), (60, 100)]  # Initial snake
    direction = "RIGHT"  # Initial direction
    next_direction = direction  # To prevent instant direction changes
    food = generate_food(snake)
    super_snack = None
    snale_snack = None
    speed_snack = None
    super_snack_timer = 0
    snale_snack_timer = 0
    speed_snack_timer = 0
    score = 0
    running = True
    current_fps = FPS

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    next_direction = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    next_direction = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    next_direction = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    next_direction = "RIGHT"

        # Update direction only at the start of each frame
        direction = next_direction

        # Move snake
        move_snake(snake, direction)

        # Check for collisions
        if check_collision(snake):
            if game_over_screen(score):  # Restart if 'R' is pressed
                return main()
            else:
                return

        # Check if food is eaten
        if check_food_collision(snake, food):
            snake.append(snake[-1])  # Grow the snake
            score += 1
            food = generate_food(snake)  # Generate new food position

        # Check if super snack is eaten
        if super_snack and check_food_collision(snake, super_snack):
            snake.append(snake[-1])  # Grow the snake
            score += 5
            super_snack = None

        # Check if snale snack is eaten
        if snale_snack and check_food_collision(snake, snale_snack):
            current_fps = max(FPS * 0.7, 1)
            snale_snack_timer = 10 * FPS
            snale_snack = None

        # Check if speed snack is eaten
        if speed_snack and check_food_collision(snake, speed_snack):
            current_fps = FPS * 1.3
            speed_snack_timer = 10 * FPS
            speed_snack = None

        # Update timers
        if snale_snack_timer > 0:
            snale_snack_timer -= 1
            if snale_snack_timer == 0:
                current_fps = FPS

        if speed_snack_timer > 0:
            speed_snack_timer -= 1
            if speed_snack_timer == 0:
                current_fps = FPS

        # Randomly spawn additional snacks
        if not super_snack and random.random() < 0.01:
            super_snack = generate_food(snake)
        if not snale_snack and random.random() < 0.01:
            snale_snack = generate_food(snake)
        if not speed_snack and random.random() < 0.01:
            speed_snack = generate_food(snake)

        # Clear screen
        screen.fill(BLACK)

        # Draw elements
        draw_border()
        draw_snake(snake)
        draw_food(food, RED)
        if super_snack:
            draw_food(super_snack, SUPER_SNACK_COLOR)
        if snale_snack:
            draw_food(snale_snack, SNALE_SNACK_COLOR)
        if speed_snack:
            draw_food(speed_snack, SPEED_SNACK_COLOR)
        draw_score(score)

        # Update display
        pygame.display.flip()

        # Control game speed
        clock.tick(current_fps)

    pygame.quit()

if __name__ == "__main__":
    main()
