import streamlit as st
import pygame
import random
import imageio

# Initialize Pygame
pygame.init()

# Set up the game window
WIDTH = 800
HEIGHT = 600
win = pygame.Surface((WIDTH, HEIGHT))
pygame.display.set_caption("MODEL Chimtu")

# Define colors
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Define block properties
BLOCK_SIZE = 50
BLOCK_SPEED = 5

# Define player properties
player_width = 50
player_height = 50
player_x = WIDTH // 2 - player_width // 2
player_y = HEIGHT // 2 - player_height // 2
player_speed = 10

clock = pygame.time.Clock()

# Generate initial block positions
block_positions = []
for _ in range(3):
    block_x = random.randint(WIDTH, WIDTH + 300)
    block_y = random.randint(0, HEIGHT - BLOCK_SIZE)
    block_positions.append((block_x, block_y))

# Game states
game_over = False

# Load font
font = pygame.font.Font(None, 36)

# Load background music
pygame.mixer.music.load("Fluffing-a-Duck.mp3")
pygame.mixer.music.set_volume(0.5)  # Adjust volume (0.0 to 1.0)

# Start playing background music
pygame.mixer.music.play(-1)  # -1 means loop indefinitely

# Load player image
player_image = pygame.image.load("chimtu1.png")
player_image = pygame.transform.scale(player_image, (player_width, player_height))

# Load game over GIF
game_over_gif = imageio.mimread("chumtu-gif (1).gif")
rotated_gif_frames = []
for frame in game_over_gif:
    pygame_image = pygame.surfarray.make_surface(frame)
    rotated_image = pygame.transform.rotate(pygame_image, -90)  # Rotate the frame by 90 degrees clockwise
    rotated_gif_frames.append(rotated_image)

# Load block images
block_images = []
for i in range(3):
    block_image = pygame.image.load(f"chimtu.png")
    block_image = pygame.transform.scale(block_image, (BLOCK_SIZE, BLOCK_SIZE))
    block_images.append(block_image)

# Streamlit App
def main():
    st.title("MODEL Chimtu")

    # Initialize Pygame surface
    pygame_surface = pygame.display.set_mode((WIDTH, HEIGHT))

    # Game loop
    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        keys = pygame.key.get_pressed()
        if not game_over:
            if keys[pygame.K_UP]:
                player_y -= player_speed
            if keys[pygame.K_DOWN]:
                player_y += player_speed
            if keys[pygame.K_LEFT]:
                player_x -= player_speed
            if keys[pygame.K_RIGHT]:
                player_x += player_speed

            player_x = max(0, min(player_x, WIDTH - player_width))
            player_y = max(0, min(player_y, HEIGHT - player_height))

            for i in range(len(block_positions)):
                block_x, block_y = block_positions[i]
                block_x -= BLOCK_SPEED
                if block_x + BLOCK_SIZE < 0:
                    block_x = WIDTH + 300
                    block_y = random.randint(0, HEIGHT - BLOCK_SIZE)
                block_positions[i] = (block_x, block_y)

                if pygame.Rect(player_x, player_y, player_width, player_height).colliderect(
                        pygame.Rect(block_x, block_y, BLOCK_SIZE, BLOCK_SIZE)):
                    game_over = True

            distance += BLOCK_SPEED

            # Calculate the score based on elapsed time
            current_time = pygame.time.get_ticks()
            elapsed_time = current_time - start_time
            score = elapsed_time // 100  # Increase the score by 1 every 0.1 seconds

        pygame_surface.fill(BLACK)

        if game_over:
            pygame.mixer.music.stop()
            game_over_text = font.render("Game Over", True, WHITE)
            game_over_text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame_surface.blit(game_over_text, game_over_text_rect)

            pygame_surface.blit(rotated_gif_frames[gif_frame_index],
                     ((WIDTH - rotated_gif_frames[gif_frame_index].get_width()) // 2,
                      (HEIGHT - rotated_gif_frames[gif_frame_index].get_height()) // 2))

            # Update the frame
            if pygame.time.get_ticks() >= frame_timer:
                gif_frame_index = (gif_frame_index + 1) % len(rotated_gif_frames)  # Update the current frame index
                frame_timer = pygame.time.get_ticks() + frame_delay

            if not game_over_sound_played:
                pygame.mixer.music.stop()
                game_over_sound = pygame.mixer.Sound("Enjoy Pandago - Notification Sound.mp3")
                game_over_sound.play()
                game_over_sound_played = True

        else:
            for block_x, block_y in block_positions:
                # Draw block images instead of red boxes
                block_image_index = block_positions.index((block_x, block_y))
                pygame_surface.blit(block_images[block_image_index], (block_x, block_y))

            pygame_surface.blit(player_image, (player_x, player_y))

            # Display the score in the top right corner
            score_text = font.render(str(score), True, WHITE)
            score_text_rect = score_text.get_rect()
            score_text_rect.topright = (WIDTH - 10, 10)
            pygame_surface.blit(score_text, score_text_rect)

        # Convert the Pygame surface to a Streamlit image
        pygame_image = pygame.surfarray.array3d(pygame_surface)
        st.image(pygame_image, channels="RGB")

if __name__ == "__main__":
    main()
