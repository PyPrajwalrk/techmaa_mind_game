import pygame
import random
import sys
import time

# Initialize Pygame & Sound System
pygame.init()
pygame.mixer.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mind Architect")

# Colors
BACKGROUND_COLOR = (20, 20, 30)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 150, 250)
HOVER_COLOR = (100, 200, 250)

# Font
FONT = pygame.font.SysFont("Arial", 36)
SMALL_FONT = pygame.font.SysFont("Arial", 28)

# Game variables
level = 1  # Starting level
score = 0
game_over = False

# Load Sound Effects (Add your own files here)
win_sound = pygame.mixer.Sound("win_sound.wav")
lose_sound = pygame.mixer.Sound("lose_sound.wav")
click_sound = pygame.mixer.Sound("click_sound.wav")

# Load Background Image
background_image = pygame.image.load("background.jpg")
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect(center=(x, y))
    surface.blit(text_obj, text_rect)

def draw_button(text, x, y, w, h, normal_color, hover_color):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    rect = pygame.Rect(x, y, w, h)
    
    if rect.collidepoint(mouse):
        pygame.draw.rect(SCREEN, hover_color, rect, border_radius=10)
        if click[0] == 1:
            pygame.mixer.Sound.play(click_sound)
            return True
    else:
        pygame.draw.rect(SCREEN, normal_color, rect, border_radius=10)
    
    draw_text(text, SMALL_FONT, TEXT_COLOR, SCREEN, x + w // 2, y + h // 2)
    return False

def generate_puzzle(level):
    """ Generates a puzzle based on the level (Increases difficulty) """
    return [random.randint(1, 9) for _ in range(level + 2)]

def play_puzzle(puzzle):
    global score, level, game_over
    
    SCREEN.blit(background_image, (0, 0))
    draw_text("Memorize the Numbers!", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 3)
    pygame.display.flip()
    
    time.sleep(1)
    SCREEN.blit(background_image, (0, 0))
    
    # Display puzzle elements with animations
    for number in puzzle:
        draw_text(str(number), FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        time.sleep(0.8)
        SCREEN.blit(background_image, (0, 0))
        pygame.display.flip()
        time.sleep(0.2)
    
    user_input = ""
    while True:
        SCREEN.blit(background_image, (0, 0))
        draw_text(f"Enter the sequence (Level {level})", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)
        draw_text(user_input, FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if user_input == ''.join(map(str, puzzle)):
                        pygame.mixer.Sound.play(win_sound)
                        score += 10 * level
                        level += 1  # Progress to the next level
                        return True
                    else:
                        pygame.mixer.Sound.play(lose_sound)
                        return False
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

# Main game loop
while True:
    if level > 10:  # Maximum level of difficulty
        SCREEN.blit(background_image, (0, 0))
        draw_text("🎉 Congratulations! You Completed the Mind Architect! 🎉", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2)
        draw_text(f"Your Score: {score}", SMALL_FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 2 + 60)
        pygame.display.flip()
        pygame.time.wait(3000)
        break
    
    SCREEN.blit(background_image, (0, 0))
    draw_text(f"Level: {level}", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4)
    draw_text(f"Score: {score}", FONT, TEXT_COLOR, SCREEN, WIDTH // 2, HEIGHT // 4 + 50)

    if draw_button("Start Puzzle", WIDTH // 2 - 100, HEIGHT // 2 - 30, 200, 60, BUTTON_COLOR, HOVER_COLOR):
        puzzle = generate_puzzle(level)
        play_puzzle(puzzle)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    
    pygame.display.flip()
