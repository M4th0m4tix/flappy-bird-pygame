import pygame
import random
import sys
import random
import math

# Initialize Pygame
pygame.init()

# Set up the display
screen_width = 800
screen_height = 1200
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Silly Flappy")

# Grass height (adjustable)
grass_height = 150  # Adjust this to the height of the green part of the image

# Global variables
floor_x_pos = 0
player_health = 6
coins_collected = 0
drones_left = 0
game_bird_y_pos = 200
game_bird_y_speed = 0
rotation_angle = 0
current_level = 1
unlocked_levels = 1
total_coins = 0
level_coins = [0] * 10
max_level_coins = [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]  # Maximum coins for each level
show_hitboxes = False
FLOOR_HITBOX_OFFSET = 0  # Adjust this value to change the floor's hitbox height
show_progress_bar = True
show_region_level = True

# Load bird images and scale them differently for each screen
home_bird_img = pygame.image.load("bird.png")  # Bird for the home screen
home_bird_img = pygame.transform.scale(home_bird_img, (210, 210))  # Larger bird on the home screen

game_bird_img = pygame.image.load("bird.png")  # Bird for the game screen
game_bird_img = pygame.transform.scale(game_bird_img, (180, 180))  # Slightly smaller bird on the game screen

# Load the floor image and scale it to fit the screen width and adjust its height
floor_img = pygame.image.load("floor.png")  # Load the provided floor.png from the same directory
floor_img = pygame.transform.scale(floor_img, (screen_width, grass_height))  # Scale the grass height using grass_height variable

# Load sun and background images for both screens
home_sun_img = pygame.image.load("sun.png")  # Load the sun for the home screen
home_sun_img = pygame.transform.scale(home_sun_img, (150, 150))  # Scale it for the home screen

game_sun_img = pygame.image.load("sun.png")  # Load the sun for the game screen
game_sun_img = pygame.transform.scale(game_sun_img, (160, 160))  # Scale it for the game screen

# Sun and background positions for the home screen
home_sun_x_pos = 600
home_sun_y_pos = 50

# Sun and background positions for the game screen
game_sun_x_pos = 600
game_sun_y_pos = 50

# Load the background image and maintain its aspect ratio
background_img = pygame.image.load("background.png")
background_aspect_ratio = background_img.get_width() / background_img.get_height()
background_scaled_height = int(screen_width / background_aspect_ratio)
background_img = pygame.transform.scale(background_img, (screen_width, background_scaled_height))

# Load enemy (drone) and coin images and scale them down
drone_img = pygame.image.load("transparent_drone.png")  # Use the transparent drone image
drone_img = pygame.transform.scale(drone_img, (120, 120))  # Scale down the drone image

coin_img = pygame.image.load("coin.png")
coin_img = pygame.transform.scale(coin_img, (90, 90))  # Scale down the coin image

# Load a separate, smaller coin image for displaying the number of collected coins
display_coin_img = pygame.transform.scale(coin_img, (60, 60))  # Increased from (30, 30)

# Define filler color (background of the background image)
background_filler = (0, 153, 204)  # Use the RGB color of the background in the provided background image

# Manually adjust the height of the background image
background_y_offset = -190  # Adjust this value to move the background image up or down

# Load custom font for the title and other text (make sure the font file is in the same directory)
whacky_font = pygame.font.Font("WhackyFont.ttf", 100)  # Replace with your downloaded font
button_font = pygame.font.Font(None, 90)  # Slightly smaller font size for buttons
info_font = pygame.font.Font(None, 60)  # Font for displaying game information

# Define colors
white = (255, 255, 255)
black = (0, 0, 0)
floor_filler = (222, 216, 149)
cyan = (113, 197, 207)
dark_gray = (40, 40, 40)  # Hex: #333333

# Title text
title_text = whacky_font.render("Silly Flappy", True, dark_gray)

# Menu options text
play_text = button_font.render("Play", True, dark_gray)
settings_text = button_font.render("Settings", True, dark_gray)
help_text = button_font.render("Help", True, dark_gray)
levels_text = button_font.render("Levels", True, dark_gray)

# Initial floor positions
floor_y_pos = screen_height - (grass_height + 50)  # Adjust position to account for the new grass height
home_screen_floor_speed = 0.3  # Slower speed of the moving floor for the home screen
game_screen_floor_speed = 1.5  # Adjusted speed of the moving floor for the game screen

# Bird properties for the home screen
home_bird_x_pos = screen_width // 2 - 430  # Position for the home screen bird
home_bird_y_pos = 125  # Adjusted vertical position for the home screen bird

# Bird properties for the game screen
game_bird_x_pos = 80  # Move the bird slightly more to the left
game_bird_y_pos = 200
game_bird_y_speed = 0
gravity = 0.3  # Increased gravity
jump_speed = -8  # Jump speed for higher jumps
rotation_angle = 0  # Start with no rotation
max_upward_angle = 25  # Maximum tilt up angle when jumping
max_downward_angle = -90  # Maximum tilt down angle when falling
rotation_speed = 1  # Speed of rotation when tilting up or down

# Game information
coins_collected = 0
region = "City"
level = 1
total_drones = 20
drones_left = total_drones
player_health = 6  # 6 half-hearts, which is 3 full hearts

# Add this function to draw hitboxes
def draw_hitbox(surface, hitbox, color=(255, 0, 0)):
    if isinstance(hitbox, list):
        if len(hitbox) > 2:
            pygame.draw.polygon(surface, color, hitbox, 2)
        else:
            print("Invalid hitbox:", hitbox)
    elif isinstance(hitbox, pygame.Rect):
        pygame.draw.rect(surface, color, hitbox, 2)
    else:
        print("Invalid hitbox:", hitbox)

# Function to display game information
def display_game_info(coins_collected, drones_destroyed, total_drones):
    # Always display coin
    coin_text = info_font.render(f"{coins_collected}", True, black)
    screen.blit(display_coin_img, (10, 10))
    screen.blit(coin_text, (80, 25))

    if show_progress_bar:
        progress = (drones_destroyed / total_drones) * 100
        progress_text = info_font.render(f"Progress: {int(progress)}%", True, black)
        screen.blit(progress_text, (10, 80))

    if show_region_level:
        region_text = info_font.render(f"Region: {region}", True, black)
        level_text = info_font.render(f"Level: {current_level}", True, black)
        screen.blit(region_text, (10, 140))
        screen.blit(level_text, (10, 200))

# Function to spawn drones and coins over time
def spawn_entities(drones, coins, duration):
    entity_interval = duration / (drones + coins)
    all_spawn_times = [i * entity_interval for i in range(drones + coins)]
    random.shuffle(all_spawn_times)
    
    drone_spawn_times = all_spawn_times[:drones]
    coin_spawn_times = all_spawn_times[drones:]
    
    return sorted(drone_spawn_times), sorted(coin_spawn_times)

# Main loop for the main menu
def main_menu():
    global floor_x_pos, player_health, coins_collected, drones_left, game_bird_y_pos, game_bird_y_speed, rotation_angle, current_level, unlocked_levels, total_coins, level_coins, show_hitboxes
    
    # Reset game state
    floor_x_pos = 0
    player_health = 6
    coins_collected = 0
    drones_left = 0
    game_bird_y_pos = 200
    game_bird_y_speed = 0
    rotation_angle = 0
    unlocked_levels = 1
    total_coins = 0
    level_coins = [0] * 10
    show_hitboxes = False

    # Create button rectangles
    button_width = 200
    button_height = 50
    button_spacing = 70  # Consistent spacing between buttons
    first_button_y = 380  # Moved up from 420
    play_button = pygame.Rect(screen_width // 2 - button_width // 2, first_button_y, button_width, button_height)
    levels_button = pygame.Rect(screen_width // 2 - button_width // 2, first_button_y + button_height + button_spacing, button_width, button_height)
    settings_button = pygame.Rect(screen_width // 2 - button_width // 2, first_button_y + 2 * (button_height + button_spacing), button_width, button_height)
    help_button = pygame.Rect(screen_width // 2 - button_width // 2, first_button_y + 3 * (button_height + button_spacing), button_width, button_height)

    # Load coin image for menu
    menu_coin_img = pygame.image.load("coin.png")
    menu_coin_img = pygame.transform.scale(menu_coin_img, (40, 40))  # Adjust size as needed

    while True:
        screen.fill(background_filler)
        
        # Draw background and sun on the home screen
        screen.blit(background_img, (0, screen_height - background_scaled_height + background_y_offset))
        screen.blit(home_sun_img, (home_sun_x_pos, home_sun_y_pos))

        # Draw title and bird icon
        title_rect = title_text.get_rect(center=(screen_width // 2 + 40, 240))
        screen.blit(title_text, title_rect)
        screen.blit(home_bird_img, (home_bird_x_pos, home_bird_y_pos))

        # Draw menu options
        play_text_rect = play_text.get_rect(center=play_button.center)
        levels_text_rect = levels_text.get_rect(center=levels_button.center)
        settings_text_rect = settings_text.get_rect(center=settings_button.center)
        help_text_rect = help_text.get_rect(center=help_button.center)

        screen.blit(play_text, play_text_rect)
        screen.blit(levels_text, levels_text_rect)
        screen.blit(settings_text, settings_text_rect)
        screen.blit(help_text, help_text_rect)

        # Draw total coins collected with coin icon
        coin_icon_rect = menu_coin_img.get_rect(topleft=(20, 20))
        screen.blit(menu_coin_img, coin_icon_rect)
        coin_text = info_font.render(f"{total_coins}", True, dark_gray)
        coin_text_rect = coin_text.get_rect(midleft=(coin_icon_rect.right + 10, coin_icon_rect.centery))
        screen.blit(coin_text, coin_text_rect)

        # Fill the space below the grass with floor_filler color
        pygame.draw.rect(screen, floor_filler, (0, floor_y_pos + grass_height, screen_width, screen_height - (floor_y_pos + grass_height)))

        # Draw and move the floor (grass)
        screen.blit(floor_img, (floor_x_pos, floor_y_pos))
        screen.blit(floor_img, (floor_x_pos + screen_width, floor_y_pos))

        floor_x_pos -= home_screen_floor_speed
        if floor_x_pos <= -screen_width:
            floor_x_pos = 0

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if play_button.collidepoint(mouse_pos):
                    game_screen()
                elif levels_button.collidepoint(mouse_pos):
                    levels_screen()
                elif settings_button.collidepoint(mouse_pos):
                    settings_screen()
                elif help_button.collidepoint(mouse_pos):
                    print("Help clicked")  # Replace with help function when implemented

        # Update the display
        pygame.display.update()

# Game screen where you control Flappy
def game_screen():
    global floor_x_pos, current_level, unlocked_levels, total_coins, level_coins, drones_left, coins_collected, player_health, game_bird_y_pos, game_bird_y_speed, rotation_angle, show_hitboxes

    floor_x_pos = 0

    # Set number of drones and coins based on current level
    total_drones = 10 + (current_level - 1) * 2  # Increase drones by 2 for each level
    drones_left = total_drones
    drones_destroyed = 0
    coins_collected = level_coins[current_level - 1]
    max_coins = max_level_coins[current_level - 1]

    # Calculate remaining coins for this level
    remaining_coins = max_coins - coins_collected

    # Time variables for spawning entities
    total_time = 20  # Total time (in seconds) over which entities will spawn
    drone_spawn_times, coin_spawn_times = spawn_entities(total_drones, remaining_coins, total_time)
    drone_spawn_times = [time * 1000 for time in drone_spawn_times]  # Convert to milliseconds
    coin_spawn_times = [time * 1000 for time in coin_spawn_times]  # Convert to milliseconds

    # Timer to keep track of elapsed time
    start_time = pygame.time.get_ticks()
    
    entities = []  # List to store spawned entities

    print(f"Starting level with {total_drones} drones")  # Debug print

    def rotate_point(x, y, angle):
        """Rotate a point around the origin."""
        rad = math.radians(angle)
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        return x * cos_a - y * sin_a, x * sin_a + y * cos_a

    def get_rotated_hitbox(rect, angle):
        """Create a single rotated rectangle to represent the bird's hitbox."""
        center_x, center_y = rect.center
        
        # Create a smaller rectangle for the hitbox
        hitbox_width = rect.width * 0.5  # Adjust this value to fit your bird sprite
        hitbox_height = rect.height * 0.4  # Adjust this value to fit your bird sprite

        # Calculate the points of the hitbox rectangle
        half_w, half_h = hitbox_width / 2, hitbox_height / 2
        points = [
            (-half_w, -half_h),
            (half_w, -half_h),
            (half_w, half_h),
            (-half_w, half_h)
        ]

        # Rotate the hitbox
        rad = math.radians(-angle)  # Negative angle to correct the rotation
        cos_a, sin_a = math.cos(rad), math.sin(rad)
        
        rotated_points = [
            (p[0] * cos_a - p[1] * sin_a + center_x, p[0] * sin_a + p[1] * cos_a + center_y)
            for p in points
        ]

        return rotated_points

    heart_img = pygame.image.load("hearts.png")
    heart_img = pygame.transform.scale(heart_img, (150, 50))  # Adjust size as needed

    def draw_hearts(health):
        heart_width = heart_img.get_width() // 3
        start_x = screen_width // 2 - (heart_width * 3) // 2
        for i in range(3):
            if health >= 2:
                screen.blit(heart_img, (start_x + i * heart_width, 10), (0, 0, heart_width, heart_img.get_height()))
            elif health == 1:
                screen.blit(heart_img, (start_x + i * heart_width, 10), (heart_width, 0, heart_width, heart_img.get_height()))
            else:
                screen.blit(heart_img, (start_x + i * heart_width, 10), (heart_width * 2, 0, heart_width, heart_img.get_height()))
            health -= 2

    clock = pygame.time.Clock()

    while True:
        screen.fill(background_filler)

        # Draw background and sun on the game screen
        screen.blit(background_img, (0, screen_height - background_scaled_height + background_y_offset))
        screen.blit(game_sun_img, (game_sun_x_pos, game_sun_y_pos))

        # Bird movement logic
        game_bird_y_speed += gravity
        game_bird_y_pos += game_bird_y_speed

        # Rotate the bird based on its vertical speed
        if game_bird_y_speed < 0:
            # Gradually tilt up when jumping
            rotation_angle = min(rotation_angle + rotation_speed, max_upward_angle)
        else:
            # Gradually tilt down when falling
            rotation_angle = max(rotation_angle - rotation_speed, max_downward_angle)

        rotated_bird_img = pygame.transform.rotate(game_bird_img, rotation_angle)
        bird_rect = game_bird_img.get_rect(center=(game_bird_x_pos + game_bird_img.get_width() // 2, game_bird_y_pos + game_bird_img.get_height() // 2))
        bird_hitbox = get_rotated_hitbox(bird_rect, rotation_angle)

        # Check if bird has hit the ground
        if game_bird_y_pos > screen_height - grass_height - rotated_bird_img.get_height() + 10:
            return ground_death_screen()  # Call the new ground death screen

        # Keep the bird within the screen bounds with increased upward range
        if game_bird_y_pos < -50:  # Allow bird to go higher above the screen
            game_bird_y_pos = -50
            game_bird_y_speed = 0
        elif game_bird_y_pos > screen_height - grass_height - rotated_bird_img.get_height() + 10:
            game_bird_y_pos = screen_height - grass_height - rotated_bird_img.get_height() + 10
            game_bird_y_speed = 0

        # Draw the rotated bird
        screen.blit(rotated_bird_img, rotated_bird_img.get_rect(center=bird_rect.center))

        # Draw and move the floor (grass)
        screen.blit(floor_img, (floor_x_pos, floor_y_pos))
        screen.blit(floor_img, (floor_x_pos + screen_width, floor_y_pos))  # Draw the second floor image next to the first

        floor_x_pos -= game_screen_floor_speed  # Move the floor left at the game screen speed
        if floor_x_pos <= -screen_width:
            floor_x_pos = 0  # Reset floor position when it's fully off the screen

        # Fill the space below the grass with floor_filler color
        pygame.draw.rect(screen, floor_filler, (0, floor_y_pos + grass_height, screen_width, screen_height - (floor_y_pos + grass_height)))

        # Spawn drones and coins over time
        elapsed_time = pygame.time.get_ticks() - start_time
        if drone_spawn_times and elapsed_time >= drone_spawn_times[0]:
            drone_spawn_times.pop(0)
            drone_x = screen_width + random.randint(0, 100)  # Spawn drone off-screen to the right
            drone_y = random.randint(50, screen_height - grass_height - drone_img.get_height() - 50)
            entities.append({"type": "drone", "rect": pygame.Rect(drone_x, drone_y, drone_img.get_width(), drone_img.get_height())})
            print(f"Spawned drone. Total entities: {len(entities)}")  # Debug print

        if coin_spawn_times and elapsed_time >= coin_spawn_times[0]:
            coin_spawn_times.pop(0)
            coin_x = screen_width + random.randint(0, 100)  # Spawn coin off-screen to the right
            coin_y = random.randint(50, screen_height - grass_height - coin_img.get_height() - 50)
            entities.append({"type": "coin", "rect": pygame.Rect(coin_x, coin_y, coin_img.get_width(), coin_img.get_height())})

        # Move and draw entities
        for entity in entities[:]:
            if entity["type"] == "drone":
                entity["rect"].x -= game_screen_floor_speed * 6
                screen.blit(drone_img, entity["rect"].topleft)
                drone_hitbox = entity["rect"].inflate(-10, -10)
                if show_hitboxes:
                    draw_hitbox(screen, drone_hitbox, (255, 0, 0))
                if any(drone_hitbox.collidepoint(point) for point in bird_hitbox):
                    print("Collided with drone!")
                    entities.remove(entity)
                    drones_destroyed += 1  # Increment destroyed drones
                    print(f"Drone destroyed. Total destroyed: {drones_destroyed}")  # Debug print
                    player_health -= 1
                    if player_health <= 0:
                        return drone_death_screen()  # Call the new death screen
            elif entity["type"] == "coin":
                entity["rect"].x -= game_screen_floor_speed * 6
                screen.blit(coin_img, entity["rect"].topleft)
                coin_hitbox = entity["rect"].inflate(-5, -5)
                if show_hitboxes:
                    draw_hitbox(screen, coin_hitbox, (0, 255, 0))
                if any(coin_hitbox.collidepoint(point) for point in bird_hitbox):
                    coins_collected += 1
                    entities.remove(entity)

            if entity["rect"].right < 0:
                if entity["type"] == "drone":
                    drones_destroyed += 1  # Count drones that go off-screen as destroyed
                    print(f"Drone went off-screen. Total destroyed: {drones_destroyed}")  # Debug print
                entities.remove(entity)

        # Draw hitboxes if enabled
        if show_hitboxes:
            draw_hitbox(screen, bird_hitbox, (0, 0, 255))  # Blue for the bird
            for entity in entities:
                if entity["type"] == "drone":
                    draw_hitbox(screen, entity["rect"].inflate(-10, -10), (255, 0, 0))
                elif entity["type"] == "coin":
                    draw_hitbox(screen, entity["rect"].inflate(-5, -5), (0, 255, 0))

        # Display game information based on settings
        display_game_info(coins_collected, drones_destroyed, total_drones)

        # Draw hearts
        draw_hearts(player_health)

        # Update the progress calculation
        progress = (drones_destroyed / total_drones) * 100
        print(f"Progress: {progress}%")  # Debug print
        progress_text = info_font.render(f"Progress: {int(progress)}%", True, black)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_bird_y_speed = jump_speed
                elif event.key == pygame.K_h:  # Press 'H' to toggle hitboxes
                    show_hitboxes = not show_hitboxes
                    print(f"Toggled show_hitboxes to: {show_hitboxes}")
                elif event.key == pygame.K_t:
                    test_screen()  # Go to the test screen

        # Check if level is complete
        if drones_destroyed == total_drones:
            print("Level complete!")  # Debug print
            level_complete_screen()
            return  # Return to levels screen after level completion

        pygame.display.update()
        clock.tick(60)  # Limit to 60 frames per second for smoother movement

def level_complete_screen():
    global current_level, unlocked_levels, total_coins, level_coins, player_health, max_level_coins

    coins_collected_this_run = min(coins_collected - level_coins[current_level - 1], max_level_coins[current_level - 1] - level_coins[current_level - 1])
    level_coins[current_level - 1] += coins_collected_this_run
    total_coins += coins_collected_this_run

    if current_level == unlocked_levels and unlocked_levels < 10:
        unlocked_levels += 1

    back_button = pygame.Rect(screen_width // 2 - 100, 500, 200, 50)

    while True:
        screen.fill(background_filler)
        
        congrats_text = whacky_font.render("Level Complete!", True, (0, 255, 0))
        congrats_rect = congrats_text.get_rect(center=(screen_width // 2, 300))
        screen.blit(congrats_text, congrats_rect)

        coins_text = info_font.render(f"Coins collected: {coins_collected_this_run}", True, dark_gray)
        coins_rect = coins_text.get_rect(center=(screen_width // 2, 400))
        screen.blit(coins_text, coins_rect)

        back_text = button_font.render("Back to Levels", True, dark_gray)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return levels_screen()  # Return to levels screen

        pygame.display.update()

def settings_screen():
    global show_hitboxes, show_progress_bar, show_region_level, floor_x_pos
    floor_x_pos = 0

    # Create button rectangles
    button_width = 300
    button_height = 50
    hitbox_button = pygame.Rect(screen_width // 2 - button_width // 2, 300, button_width, button_height)
    progress_button = pygame.Rect(screen_width // 2 - button_width // 2, 400, button_width, button_height)
    region_button = pygame.Rect(screen_width // 2 - button_width // 2, 500, button_width, button_height)
    back_button = pygame.Rect(screen_width // 2 - button_width // 2, 600, button_width, button_height)

    while True:
        screen.fill(background_filler)
        
        # Draw background
        screen.blit(background_img, (0, screen_height - background_scaled_height + background_y_offset))

        # Draw and move the floor (grass)
        screen.blit(floor_img, (floor_x_pos, floor_y_pos))
        screen.blit(floor_img, (floor_x_pos + screen_width, floor_y_pos))

        floor_x_pos -= home_screen_floor_speed
        if floor_x_pos <= -screen_width:
            floor_x_pos = 0

        # Fill the space below the grass with floor_filler color
        pygame.draw.rect(screen, floor_filler, (0, floor_y_pos + grass_height, screen_width, screen_height - (floor_y_pos + grass_height)))

        # Draw title
        settings_text = whacky_font.render("Settings", True, dark_gray)
        settings_text_rect = settings_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(settings_text, settings_text_rect)

        # Draw buttons
        hitbox_text = button_font.render(f"Show Hitboxes: {'On' if show_hitboxes else 'Off'}", True, dark_gray)
        progress_text = button_font.render(f"Show Progress: {'On' if show_progress_bar else 'Off'}", True, dark_gray)
        region_text = button_font.render(f"Show Region/Level: {'On' if show_region_level else 'Off'}", True, dark_gray)
        back_text = button_font.render("Back to Menu", True, dark_gray)

        hitbox_text_rect = hitbox_text.get_rect(center=hitbox_button.center)
        progress_text_rect = progress_text.get_rect(center=progress_button.center)
        region_text_rect = region_text.get_rect(center=region_button.center)
        back_text_rect = back_text.get_rect(center=back_button.center)

        screen.blit(hitbox_text, hitbox_text_rect)
        screen.blit(progress_text, progress_text_rect)
        screen.blit(region_text, region_text_rect)
        screen.blit(back_text, back_text_rect)

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if hitbox_button.collidepoint(mouse_pos):
                    show_hitboxes = not show_hitboxes
                elif progress_button.collidepoint(mouse_pos):
                    show_progress_bar = not show_progress_bar
                elif region_button.collidepoint(mouse_pos):
                    show_region_level = not show_region_level
                elif back_button.collidepoint(mouse_pos):
                    return  # Go back to main menu

        pygame.display.update()

def game_over_screen():
    global player_health, coins_collected, drones_left, game_bird_y_pos, game_bird_y_speed, rotation_angle, current_level, unlocked_levels, total_coins, level_coins

    retry_button = pygame.Rect(screen_width // 2 - 100, 500, 200, 50)

    while True:
        screen.fill(background_filler)
        
        # Draw "You Lose" text
        lose_text = whacky_font.render("You Lose", True, (255, 0, 0))
        lose_text_rect = lose_text.get_rect(center=(screen_width // 2, 300))
        screen.blit(lose_text, lose_text_rect)

        # Draw retry button
        retry_text = button_font.render("Retry", True, dark_gray)
        retry_text_rect = retry_text.get_rect(center=retry_button.center)
        screen.blit(retry_text, retry_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if retry_button.collidepoint(event.pos):
                    # Reset all progress
                    player_health = 6
                    coins_collected = 0
                    drones_left = 0
                    game_bird_y_pos = 200
                    game_bird_y_speed = 0
                    rotation_angle = 0
                    current_level = 1
                    unlocked_levels = 1
                    total_coins = 0
                    level_coins = [0] * 10
                    return main_menu()  # Return to main menu

        pygame.display.update()

def levels_screen():
    global current_level, unlocked_levels, total_coins, player_health

    # Create a 3x3 grid for levels 1-9
    grid_size = 3
    level_size = 120  # Increased size
    grid_spacing = 70  # Increased spacing
    start_x = (screen_width - (grid_size * level_size + (grid_size - 1) * grid_spacing)) // 2
    start_y = 250  # Moved lower

    # Load lock image
    lock_img = pygame.image.load("lock.png")
    lock_img = pygame.transform.scale(lock_img, (60, 60))  # Slightly larger lock

    # Create back button
    back_button = pygame.Rect(screen_width - 150, 50, 100, 50)

    # Create next region button (arrow)
    next_region_button = pygame.Rect(screen_width - 150, screen_height - 100, 100, 50)

    while True:
        screen.fill(background_filler)
        
        # Draw title
        title_text = whacky_font.render("City", True, dark_gray)
        title_rect = title_text.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_text, title_rect)

        # Draw levels
        for i in range(9):
            row = i // grid_size
            col = i % grid_size
            x = start_x + col * (level_size + grid_spacing)
            y = start_y + row * (level_size + grid_spacing)
            level_rect = pygame.Rect(x, y, level_size, level_size)
            pygame.draw.rect(screen, dark_gray, level_rect, 4)  # Thicker border
            
            level_num = i + 1
            if level_num <= unlocked_levels:
                level_text = button_font.render(str(level_num), True, dark_gray)
                level_text_rect = level_text.get_rect(center=level_rect.center)
                screen.blit(level_text, level_text_rect)
            else:
                screen.blit(lock_img, lock_img.get_rect(center=level_rect.center))

        # Draw level 10
        level_10_rect = pygame.Rect(screen_width // 2 - level_size // 2, start_y + 3 * (level_size + grid_spacing), level_size, level_size)
        pygame.draw.rect(screen, dark_gray, level_10_rect, 4)  # Thicker border
        if unlocked_levels >= 10:
            level_text = button_font.render("10", True, dark_gray)
            level_text_rect = level_text.get_rect(center=level_10_rect.center)
            screen.blit(level_text, level_text_rect)
        else:
            screen.blit(lock_img, lock_img.get_rect(center=level_10_rect.center))

        # Draw back button (text only, no white box)
        back_text = button_font.render("Back", True, dark_gray)
        back_text_rect = back_text.get_rect(center=back_button.center)
        screen.blit(back_text, back_text_rect)

        # Draw next region button (arrow)
        pygame.draw.rect(screen, dark_gray, next_region_button, 2)
        arrow_width = 60
        arrow_height = 30
        arrow_x = next_region_button.centerx - arrow_width // 2
        arrow_y = next_region_button.centery - arrow_height // 2
        pygame.draw.rect(screen, dark_gray, (arrow_x, arrow_y, arrow_width * 2 // 3, arrow_height))
        pygame.draw.polygon(screen, dark_gray, [
            (arrow_x + arrow_width * 2 // 3, arrow_y),
            (arrow_x + arrow_width, arrow_y + arrow_height // 2),
            (arrow_x + arrow_width * 2 // 3, arrow_y + arrow_height)
        ])

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if back_button.collidepoint(mouse_pos):
                    return
                for i in range(10):
                    level_rect = pygame.Rect(start_x + (i % grid_size) * (level_size + grid_spacing),
                                             start_y + (i // grid_size) * (level_size + grid_spacing),
                                             level_size, level_size)
                    if i == 9:  # Level 10
                        level_rect = level_10_rect
                    if level_rect.collidepoint(mouse_pos) and i + 1 <= unlocked_levels:
                        current_level = i + 1
                        return game_screen()  # No need to pass player_health here

        pygame.display.update()

def drone_death_screen():
    global total_coins, level_coins

    # Load necessary images
    dead_flappy = pygame.image.load("dead_flappy.png")
    game_over_title = pygame.image.load("game_over.png")
    
    # Scale images while maintaining aspect ratio
    dead_flappy_width = 150  # Adjust this value as needed
    dead_flappy_height = int(dead_flappy.get_height() * (dead_flappy_width / dead_flappy.get_width()))
    dead_flappy = pygame.transform.scale(dead_flappy, (dead_flappy_width, dead_flappy_height))

    game_over_width = 800  # Increased from 300 to 400
    game_over_height = int(game_over_title.get_height() * (game_over_width / game_over_title.get_width()))
    game_over_title = pygame.transform.scale(game_over_title, (game_over_width, game_over_height))

    # Create back button
    button_width, button_height = 340, 80
    back_button = pygame.Rect(screen_width // 2 - button_width // 2, 400, button_width, button_height)

    # Create a list of drone positions on top of Flappy
    num_drones = 12  # Adjust the number of drones as needed
    flappy_center_x = screen_width // 2
    flappy_top_y = screen_height - grass_height - dead_flappy_height
    drone_positions = [
        (flappy_center_x + random.randint(-50, 50), 
         flappy_top_y + random.randint(-20, 20)) 
        for _ in range(num_drones)
    ]

    while True:
        screen.fill(background_filler)
        
        # Draw static background
        screen.blit(background_img, (0, screen_height - background_scaled_height + background_y_offset))
        screen.blit(game_sun_img, (game_sun_x_pos, game_sun_y_pos))
        
        # Draw floor
        screen.blit(floor_img, (0, floor_y_pos))
        
        # Fill the space below the grass with floor_filler color
        pygame.draw.rect(screen, floor_filler, (0, floor_y_pos + grass_height, screen_width, screen_height - (floor_y_pos + grass_height)))
        
        # Draw dead Flappy
        flappy_rect = dead_flappy.get_rect(midbottom=(screen_width // 2, screen_height - grass_height- 30))
        screen.blit(dead_flappy, flappy_rect)
        
        # Draw drones on top of Flappy
        for drone_pos in drone_positions:
            rotated_drone = pygame.transform.rotate(drone_img, random.randint(0, 360))
            drone_rect = rotated_drone.get_rect(center=drone_pos)
            screen.blit(rotated_drone, drone_rect)
        
        # Draw game over title
        title_rect = game_over_title.get_rect(center=(screen_width // 2, 300))
        screen.blit(game_over_title, title_rect)
        
        # Draw menu button
        pygame.draw.rect(screen, (50, 50, 50), back_button)  # Dark gray background
        pygame.draw.rect(screen, (200, 200, 200), back_button, 3)  # Light gray border
        
        menu_text = button_font.render("Main Menu", True, (255, 255, 255))  # White text
        menu_text_rect = menu_text.get_rect(center=back_button.center)
        screen.blit(menu_text, menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if back_button.collidepoint(event.pos):
                    return main_menu()
            elif event.type == pygame.MOUSEMOTION:
                if back_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, (70, 70, 70), back_button)  # Lighter gray on hover
                    pygame.draw.rect(screen, (220, 220, 220), back_button, 3)  # Lighter border on hover
                    screen.blit(menu_text, menu_text_rect)

        pygame.display.update()

def ground_death_screen():
    global total_coins, level_coins

    # Load necessary images
    game_over_title = pygame.image.load("game_over.png")
    nuke_background = pygame.image.load("nuke.png")
    
    # Scale images while maintaining aspect ratio
    game_over_width = 800  # Adjust this value as needed
    game_over_height = int(game_over_title.get_height() * (game_over_width / game_over_title.get_width()))
    game_over_title = pygame.transform.scale(game_over_title, (game_over_width, game_over_height))

    # Scale nuke background to fit the screen
    nuke_background = pygame.transform.scale(nuke_background, (screen_width, screen_height))

    # Create menu button
    button_width, button_height = 350, 120
    menu_button = pygame.Rect(screen_width // 2 - button_width // 2, screen_height - 150, button_width, button_height)

    while True:
        # Draw nuke background
        screen.blit(nuke_background, (0, 0))
        
        # Draw game over title
        title_rect = game_over_title.get_rect(center=(screen_width // 2, 150))
        screen.blit(game_over_title, title_rect)
        
        # Draw menu button
        pygame.draw.rect(screen, (50, 50, 50), menu_button)  # Dark gray background
        pygame.draw.rect(screen, (200, 200, 200), menu_button, 3)  # Light gray border
        
        menu_text = button_font.render("Main Menu", True, (255, 255, 255))  # White text
        menu_text_rect = menu_text.get_rect(center=menu_button.center)
        screen.blit(menu_text, menu_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if menu_button.collidepoint(event.pos):
                    return main_menu()
            elif event.type == pygame.MOUSEMOTION:
                if menu_button.collidepoint(event.pos):
                    pygame.draw.rect(screen, (70, 70, 70), menu_button)  # Lighter gray on hover
                    pygame.draw.rect(screen, (220, 220, 220), menu_button, 3)  # Lighter border on hover
                    screen.blit(menu_text, menu_text_rect)

        pygame.display.update()

# Load images for the wrecking ball and chain
try:
    chain_img = pygame.image.load("chain.png").convert_alpha()
    chain_img = pygame.transform.scale(chain_img, (1500, 800))  # Adjust size as needed
except pygame.error as e:
    print(f"Error loading chain.png: {e}")
    pygame.quit()
    sys.exit()

try:
    paper_ball_img = pygame.image.load("paper_ball.png").convert_alpha()
    paper_ball_img = pygame.transform.scale(paper_ball_img, (175, 175))  # Adjust size as needed
except pygame.error as e:
    print(f"Error loading paper_ball.png: {e}")
    pygame.quit()
    sys.exit()

def test_screen():
    running = True
    
    # Define the fixed position of the anchor point (purple dot)
    anchor_x = screen_width // 2
    anchor_y = 100  # Position near the top of the screen

    # Pendulum properties
    swing_angle = 0  # Current swing angle in radians
    swing_speed = 0.005  # Swing speed (adjust for slower or faster swinging)
    swing_direction = 1  # 1 for clockwise, -1 for counterclockwise
    max_swing_angle = math.pi / 4  # Maximum swing angle (45 degrees)
    chain_length = 600  # Length of the chain

    # Control variable for swinging
    is_swinging = False  # Start as a still image

    # Chain offset from the anchor point (allowing adjustments)
    chain_offset_x = +6
    chain_offset_y = +270

    # Rotation point offset from the anchor point
    rotation_offset_x = 0
    rotation_offset_y = 100

    # Load and scale chain image
    try:
        chain_img = pygame.image.load("chain.png").convert_alpha()
        # Ensure the chain image's width is 10 pixels and height matches chain_length
        # The pivot (top center) should be at (5, 0) if the image is 10 pixels wide
        chain_img = pygame.transform.scale(chain_img, (1000, chain_length))
    except pygame.error as e:
        print(f"Error loading chain.png: {e}")
        pygame.quit()
        sys.exit()

    # Load and scale paper ball image
    try:
        paper_ball_img = pygame.image.load("paper_ball.png").convert_alpha()
        paper_ball_img = pygame.transform.scale(paper_ball_img, (50, 50))  # Adjust size as needed
    except pygame.error as e:
        print(f"Error loading paper_ball.png: {e}")
        pygame.quit()
        sys.exit()

    # Helper function to rotate an image around its pivot
    def blit_rotate(surf, image, pos, pivot, angle):
        """
        Rotate an image and blit it to the surface.

        :param surf: Surface to blit the image onto.
        :param image: The image to rotate and blit.
        :param pos: The position of the pivot on the surface.
        :param pivot: The pivot point on the image.
        :param angle: The rotation angle in degrees.
        """
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rect = rotated_image.get_rect(center=pos)

        # Calculate the offset from the pivot to the center of the rotated image
        offset = pygame.math.Vector2(pivot).rotate(-angle)
        rotated_rect.center = (pos[0] + offset.x, pos[1] + offset.y)

        # Blit the rotated image
        surf.blit(rotated_image, rotated_rect.topleft)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_s:
                    is_swinging = not is_swinging
                # Adjust chain's x and y offset relative to the anchor
                if event.key == pygame.K_UP:
                    chain_offset_y -= 10
                if event.key == pygame.K_DOWN:
                    chain_offset_y += 10
                if event.key == pygame.K_LEFT:
                    chain_offset_x -= 10
                if event.key == pygame.K_RIGHT:
                    chain_offset_x += 10
                # Adjust rotation point offset
                if event.key == pygame.K_w:
                    rotation_offset_y -= 10
                if event.key == pygame.K_s:
                    rotation_offset_y += 10
                if event.key == pygame.K_a:
                    rotation_offset_x -= 10
                if event.key == pygame.K_d:
                    rotation_offset_x += 10

        # Fill the background
        screen.fill((0, 255, 255))  # Cyan background

        # Update swing angle if swinging is enabled
        if is_swinging:
            swing_angle += swing_speed * swing_direction
            if abs(swing_angle) > max_swing_angle:
                swing_direction *= -1  # Reverse direction at max angle

        # Calculate the rotation point
        rotation_x = anchor_x + rotation_offset_x
        rotation_y = anchor_y + rotation_offset_y

        # Calculate ball position based on swing angle and chain length
        ball_x = rotation_x + math.sin(swing_angle) * chain_length
        ball_y = rotation_y + math.cos(swing_angle) * chain_length

        # Draw the purple dot (anchor point)
        pygame.draw.circle(screen, (128, 0, 128), (anchor_x, anchor_y), 5)  # Purple dot

        # Draw the red dot at the rotation point
        pygame.draw.circle(screen, (255, 0, 0), (rotation_x, rotation_y), 5)  # Red dot for chain top

        # Rotate and blit the chain image
        # The pivot on the image is (5, 0) assuming the image width is 10
        blit_rotate(
            screen, 
            chain_img, 
            (rotation_x + chain_offset_x, rotation_y + chain_offset_y),  # Position on the screen where the pivot will be
            (5, 0),  # Pivot point on the image (top center)
            -math.degrees(swing_angle)  # Negative degrees because Pygame rotates counter-clockwise
        )

        # Rotate and blit the paper ball image
        rotated_ball_img = pygame.transform.rotate(paper_ball_img, math.degrees(swing_angle))
        ball_rect = rotated_ball_img.get_rect(center=(ball_x, ball_y))
        screen.blit(rotated_ball_img, ball_rect.topleft)

        # Draw the green dot at the center of the paper ball
        pygame.draw.circle(screen, (0, 255, 0), (ball_x, ball_y), 5)  # Green dot

        # Update the display
        pygame.display.flip()



# Run the game
if __name__ == "__main__":
    main_menu()