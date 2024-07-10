import pygame
import sys
import random
import hashlib
import time

# Initialize Pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set up the display
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Keyboard Warriors")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Game states
START, PLAYING, GAME_OVER = 0, 1, 2
state = START

# Font
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Words for the game
words = [
    "modulation", "demodulation", "bandwidth", "signal", "noise", "encoder",
    "decoder", "multiplexing", "bitrate", "amplitude", "frequency", "phase",
    "digital", "transmission", "receiver", "transmitter", "sampling", 
    "quantization", "pulse", "spectrum"
]
current_word = ""
typed_word = ""
score = 0
total_words_typed = 0
total_time_elapsed = 0

# Timer properties
initial_time = 5
time_remaining = initial_time
start_time = None

# Drifting control
drift_counter = 0
drift_interval = 20  # Change the interval to adjust drifting frequency

# Function to get a new word
def get_new_word():
    return random.choice(words)

# Function to calculate WPM
def calculate_wpm(words_typed, time_elapsed):
    if time_elapsed > 0:
        wpm = (words_typed / 5) / (time_elapsed / 60)  # Assuming an average word length of 5 characters
        return int(wpm)
    else:
        return 0

# Function to get the checksum of a word
def get_checksum(word):
    return hashlib.md5(word.encode()).hexdigest()

def start_screen():
    screen.fill(WHITE)
    text = font.render("Keyboard Warriors", True, BLACK)
    start_text = small_font.render("Press ENTER to start", True, BLACK)
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(start_text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 3 - text.get_height() // 2 + 50))
    pygame.display.flip()

def main_game_screen():
    global drift_counter
    global total_words_typed
    global total_time_elapsed
    global score
    global time_remaining
    global start_time
    screen.fill(WHITE)
    word_text = font.render(current_word, True, BLACK)
    typed_text = font.render(typed_word, True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    
    # Time bar properties
    time_bar_length = 400
    time_bar_height = 20
    time_bar_x = SCREEN_WIDTH // 2 - time_bar_length // 2
    time_bar_y = SCREEN_HEIGHT // 3 + 50
    
    # Calculate the current length of the time bar
    current_time_bar_length = int(time_bar_length * (time_remaining / initial_time))
    
    # Shaking effect if time is running out
    if time_remaining <= 1:
        offset_x = random.randint(-5, 5)
        offset_y = random.randint(-5, 5)
    else:
        offset_x = 0
        offset_y = 0
    
    # Drifting effect for the word
    if drift_counter % drift_interval == 0:
        drift_x = random.randint(-1, 1)
        drift_y = random.randint(-1, 1)
    else:
        drift_x = 0
        drift_y = 0
    
    drift_counter += 1
    
    screen.blit(word_text, (SCREEN_WIDTH // 2 - word_text.get_width() // 2 + drift_x, SCREEN_HEIGHT // 3 - word_text.get_height() // 2 + drift_y))
    screen.blit(typed_text, (SCREEN_WIDTH // 2 - typed_text.get_width() // 2, SCREEN_HEIGHT // 2 - typed_text.get_height() // 2))
    screen.blit(score_text, (10, 10))
    
    # Draw the time bar
    pygame.draw.rect(screen, RED, (time_bar_x + offset_x, time_bar_y + offset_y, time_bar_length, time_bar_height))
    pygame.draw.rect(screen, GREEN, (time_bar_x + offset_x, time_bar_y + offset_y, current_time_bar_length, time_bar_height))
    
    # Display WPM
    wpm = calculate_wpm(total_words_typed, total_time_elapsed)
    wpm_text = small_font.render(f"WPM: {wpm}", True, BLACK)
    screen.blit(wpm_text, (SCREEN_WIDTH - wpm_text.get_width() - 10, 10))
    
    pygame.display.flip()

def game_over_screen():
    global total_words_typed
    global total_time_elapsed
    global score
    screen.fill(WHITE)
    text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, BLACK)
    
    # Calculate average WPM
    average_wpm = calculate_wpm(total_words_typed, total_time_elapsed)
    average_wpm_text = small_font.render(f"Average WPM: {average_wpm}", True, BLACK)
    
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height()))
    screen.blit(average_wpm_text, (SCREEN_WIDTH // 2 - average_wpm_text.get_width() // 2, SCREEN_HEIGHT // 2 + text.get_height() + 50))
    
    pygame.display.flip()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            if state == START:
                if event.key == pygame.K_RETURN:
                    state = PLAYING
                    current_word = get_new_word()
                    typed_word = ""
                    score = 0
                    total_words_typed = 0
                    total_time_elapsed = 0
                    time_remaining = initial_time
                    start_time = time.time()
            elif state == PLAYING:
                if event.key == pygame.K_RETURN:
                    if get_checksum(typed_word) == get_checksum(current_word):
                        score += 1
                        total_words_typed += 1
                        current_word = get_new_word()
                        typed_word = ""
                        # Decrease time more gradually
                        time_remaining = max(initial_time - (score * 0.1), 1)
                        start_time = time.time()
                    else:
                        state = GAME_OVER
                elif event.key == pygame.K_BACKSPACE:
                    typed_word = typed_word[:-1]
                else:
                    typed_word += event.unicode
            elif state == GAME_OVER:
                if event.key == pygame.K_RETURN:
                    state = START

    if state == PLAYING:
        time_elapsed = time.time() - start_time
        total_time_elapsed += time_elapsed
        if time_remaining > 0:
            time_remaining -= time_elapsed
        start_time = time.time()
        if time_remaining <= 0:
            state = GAME_OVER

    if state == START:
        start_screen()
    elif state == PLAYING:
        main_game_screen()
    elif state == GAME_OVER:
        game_over_screen()
