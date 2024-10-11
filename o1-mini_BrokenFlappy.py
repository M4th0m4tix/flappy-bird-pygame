import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 1200
GRASS_HEIGHT = 220  # Adjust this to match your floor.png height
BIRD_WIDTH = 50
BIRD_HEIGHT = 50
BIRD_START_X = 100
BIRD_START_Y = 600  # Starting Y position for the bird
FLOOR_SPEED = 5  # Speed at which the floor moves
GRAVITY = 0.5
JUMP_SPEED = -10
MAX_BIRD_HEIGHT = 0  # Top limit (0 means top of the screen)
SHOW_HITBOXES = False  # Toggle to show hitboxes by default
HITBOX_COLOR = (255, 0, 0)  # Red color for hitboxes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SKY_BLUE = (135, 206, 235)

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Silly Flappy")

# Load images
try:
    floor_img = pygame.image.load("floor.png").convert_alpha()
    floor_img = pygame.transform.scale(floor_img, (SCREEN_WIDTH, GRASS_HEIGHT))
except pygame.error as e:
    print(f"Error loading floor.png: {e}")
    pygame.quit()
    sys.exit()

try:
    bird_img = pygame.image.load("bird.png").convert_alpha()
    bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
except pygame.error as e:
    print(f"Error loading bird.png: {e}")
    pygame.quit()
    sys.exit()

# Clock
clock = pygame.time.Clock()

# Global Variables
floor_y_pos = SCREEN_HEIGHT - GRASS_HEIGHT
collision_floor_y_pos = floor_y_pos  # No offset for precise collision
floor_x_pos = 0
bird_y_pos = BIRD_START_Y
bird_y_speed = 0
floor_rect = pygame.Rect(0, collision_floor_y_pos, SCREEN_WIDTH, GRASS_HEIGHT)

def reset_game_state():
    global bird_y_pos, bird_y_speed, floor_x_pos, floor_rect
    bird_y_pos = BIRD_START_Y
    bird_y_speed = 0
    floor_x_pos = 0
    # Create the floor hitbox aligned with the visual floor
    floor_rect = pygame.Rect(floor_x_pos, collision_floor_y_pos, SCREEN_WIDTH, GRASS_HEIGHT)

def main_menu():
    global SHOW_HITBOXES

    while True:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return game_screen()  # Start the game
                if event.key == pygame.K_h:
                    SHOW_HITBOXES = not SHOW_HITBOXES  # Toggle hitboxes

        # Drawing the Main Menu
        screen.fill(SKY_BLUE)  # Sky blue background

        # Display Title
        font = pygame.font.SysFont(None, 100)
        title_text = font.render("Silly Flappy", True, WHITE)
        screen.blit(title_text, (
            SCREEN_WIDTH // 2 - title_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - title_text.get_height() // 2 - 100
        ))

        # Instruction Text
        small_font = pygame.font.SysFont(None, 50)
        start_text = small_font.render("Press SPACE to Start", True, WHITE)
        screen.blit(start_text, (
            SCREEN_WIDTH // 2 - start_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - start_text.get_height() // 2
        ))

        toggle_text = small_font.render("Press 'H' to Toggle Hitboxes", True, WHITE)
        screen.blit(toggle_text, (
            SCREEN_WIDTH // 2 - toggle_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - toggle_text.get_height() // 2 + 60
        ))

        # Show hitboxes if enabled
        if SHOW_HITBOXES:
            # Draw the floor hitbox in the main menu
            floor_hitbox = pygame.Rect(floor_x_pos, floor_y_pos, SCREEN_WIDTH, GRASS_HEIGHT)
            pygame.draw.rect(screen, HITBOX_COLOR, floor_hitbox, 2)

            # Draw a dummy bird hitbox in the main menu
            bird_dummy_rect = pygame.Rect(BIRD_START_X, BIRD_START_Y, BIRD_WIDTH, BIRD_HEIGHT)
            pygame.draw.rect(screen, HITBOX_COLOR, bird_dummy_rect, 2)

        pygame.display.flip()

def game_screen():
    global bird_y_pos, bird_y_speed, floor_x_pos, floor_rect, SHOW_HITBOXES

    reset_game_state()
    running = True

    while running:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird_y_speed = JUMP_SPEED
                if event.key == pygame.K_h:
                    SHOW_HITBOXES = not SHOW_HITBOXES  # Toggle hitboxes

        # Apply gravity
        bird_y_speed += GRAVITY
        bird_y_pos += bird_y_speed

        # Constrain bird's vertical position
        if bird_y_pos < MAX_BIRD_HEIGHT:
            bird_y_pos = MAX_BIRD_HEIGHT
            bird_y_speed = 0
        elif bird_y_pos > floor_y_pos - BIRD_HEIGHT:
            bird_y_pos = floor_y_pos - BIRD_HEIGHT
            bird_y_speed = 0

        # Create bird_rect for collision detection
        bird_rect = pygame.Rect(BIRD_START_X, bird_y_pos, BIRD_WIDTH, BIRD_HEIGHT)

        # Clear screen
        screen.fill(SKY_BLUE)  # Sky blue background

        # Draw bird
        screen.blit(bird_img, (BIRD_START_X, bird_y_pos))

        # Draw and move floor
        screen.blit(floor_img, (floor_x_pos, floor_y_pos))
        screen.blit(floor_img, (floor_x_pos + SCREEN_WIDTH, floor_y_pos))

        # Move floor
        floor_x_pos -= FLOOR_SPEED
        if floor_x_pos <= -SCREEN_WIDTH:
            floor_x_pos = 0

        # Update floor_rect position as floor scrolls
        floor_rect.x = floor_x_pos

        # Show hitboxes if enabled
        if SHOW_HITBOXES:
            pygame.draw.rect(screen, HITBOX_COLOR, floor_rect, 2)  # Floor hitbox
            pygame.draw.rect(screen, HITBOX_COLOR, bird_rect, 2)   # Bird hitbox

        # Check for collision
        if bird_rect.colliderect(floor_rect):
            return ground_death_screen()

        pygame.display.flip()

def ground_death_screen():
    global SHOW_HITBOXES

    while True:
        clock.tick(60)  # 60 FPS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return game_screen()  # Restart the game
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_h:
                    SHOW_HITBOXES = not SHOW_HITBOXES  # Toggle hitboxes

        # Display Game Over Text
        screen.fill(BLACK)  # Black background

        font = pygame.font.SysFont(None, 74)
        game_over_text = font.render("Game Over", True, WHITE)
        screen.blit(game_over_text, (
            SCREEN_WIDTH // 2 - game_over_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - game_over_text.get_height() // 2 - 50
        ))

        # Instruction Text
        small_font = pygame.font.SysFont(None, 36)
        restart_text = small_font.render("Press 'R' to Restart or 'Q' to Quit", True, WHITE)
        screen.blit(restart_text, (
            SCREEN_WIDTH // 2 - restart_text.get_width() // 2,
            SCREEN_HEIGHT // 2 - restart_text.get_height() // 2 + 20
        ))

        # Show hitboxes if enabled
        if SHOW_HITBOXES:
            pygame.draw.rect(screen, HITBOX_COLOR, floor_rect, 2)  # Floor hitbox
            pygame.draw.rect(screen, HITBOX_COLOR, pygame.Rect(BIRD_START_X, bird_y_pos, BIRD_WIDTH, BIRD_HEIGHT), 2)  # Bird hitbox

        pygame.display.flip()

# Run the game
if __name__ == "__main__":
    main_menu()