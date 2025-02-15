import os
import pygame
import time
import random

pygame.font.init()

# Set up the display
WIDTH, HEIGHT = 1000, 900
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Invaders")

# Define correct paths
player_img_path = "/home/chrisamoako/Downloads/spc.jpeg"
bg_img_path = "images/1.webp"

# Check if player image exists
if not os.path.exists(player_img_path):
    print(f"Error: Image file '{player_img_path}' not found!")
    pygame.quit()
    exit()

# Load player image and scale
player_img = pygame.image.load(player_img_path)
player_img = pygame.transform.scale(player_img, (50, 50))

# Check if background image exists
if not os.path.exists(bg_img_path):
    print(f"Error: Background image '{bg_img_path}' not found!")
    pygame.quit()
    exit()

# Load and scale the background image
BG = pygame.transform.scale(pygame.image.load(bg_img_path), (WIDTH, HEIGHT))

# Player settings
PLAYER_VEL = 8
STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 40)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    # Draw player image instead of a rectangle
    WIN.blit(player_img, (player.x, player.y))

    for star in stars:
        pygame.draw.rect(WIN, "yellow", star)

    pygame.display.update()

def show_game_over():
    WIN.fill((0, 0, 0))
    lose_text = FONT.render("You Lost!", 1, "white")
    retry_text = FONT.render("Press SPACE to play again or ESC to quit", 1, "white")

    WIN.blit(lose_text, (WIDTH / 2 - lose_text.get_width() / 2, HEIGHT / 2 - lose_text.get_height() / 2))
    WIN.blit(retry_text, (WIDTH / 2 - retry_text.get_width() / 2, HEIGHT / 2 + lose_text.get_height()))

    pygame.display.update()

def main():
    run = True

    # Define player position using image rect
    player = player_img.get_rect(midbottom=(WIDTH // 2, HEIGHT - 10))

    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0

    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)  # Set frame rate to 60 FPS
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        # Handle player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        # Move stars and check collision
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y >= HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):  # Proper collision detection
                stars.remove(star)
                hit = True
                break  # Exit loop to prevent multiple detections

        if hit:
            show_game_over()

            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            main()  # Restart game
                        if event.key == pygame.K_ESCAPE:
                            pygame.quit()
                            exit()    

        draw(player, elapsed_time, stars)

    pygame.quit()

if __name__ == "__main__":
    main()