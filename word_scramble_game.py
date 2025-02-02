import pygame
import random
import time
# Initialize Pygame
pygame.init()

# Set up display
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Word Scramble Game")

# Font and font styles
font = pygame.font.Font(None, 24)  # Normal font size
title_font = pygame.font.Font(None, 30)  # Heading font size
hint_font = pygame.font.Font(None, 24)  # Font size for hints

# Colors (Elegant scheme)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)  # Background color
LIGHT_BLUE = (173, 216, 230)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
LIGHT_GREEN = (144, 238, 144)
DARK_GRAY = (169, 169, 169)

# Categories
countries = ['Pakistan', 'India', 'USA', 'Brazil', 'China', 'Japan', 'Germany', 'Australia', 'France', 'Italy']
fruits = ['apple', 'banana', 'cherry', 'kiwi', 'mango', 'orange', 'grapes', 'pear', 'pineapple', 'melon']
vegetables = ['carrot', 'tomato', 'lettuce', 'onion', 'spinach', 'potato', 'broccoli', 'cucumber', 'eggplant', 'pepper']

# Timer settings
time_limit = 15  # Time limit per question (in seconds)

# Score and level settings
score = 0
level = 1
total_levels = 15

# Scramble word function
def scramble_word(word):
    return ''.join(random.sample(word, len(word)))

# Display text function
def display_text(text, x, y, color=WHITE, font_type=font):
    label = font_type.render(text, True, color)
    screen.blit(label, (x, y))

# Timer function
def display_timer(time_left, x, y):
    timer_text = font.render(f"Time Left: {time_left}s", True, RED)
    screen.blit(timer_text, (x, y))

# Function to display letters in boxes
def display_word_in_boxes(word, x, y):
    box_width = 50
    box_height = 50
    for i, letter in enumerate(word):
        pygame.draw.rect(screen, LIGHT_BLUE, (x + i * (box_width + 10), y, box_width, box_height), 3)
        display_text(letter, x + i * (box_width + 10) + 15, y + 10, color=DARK_GRAY, font_type=title_font)

# Function to handle user input and checking the answer
def ask_question(word, scrambled_word):
    player_input = ""
    start_time = time.time()
    time_left = time_limit
    correct = False

    # Game loop for asking the question
    while not correct:
        screen.fill(BLACK)  # Fill background with black
        display_text(f"Scrambled Word: {scrambled_word}", 150, 150, LIGHT_BLUE, font_type=title_font)
        display_text("Type the correct word", 150, 220, WHITE, font_type=hint_font)
        display_word_in_boxes(player_input, 150, 300)
        
        # Display hint (First letter of the word)
        display_text(f"Hint: Starts with '{word[0].upper()}'", 150, 250, LIGHT_GREEN, font_type=hint_font)
        
        # Update the timer (ensure it doesn't go below zero)
        time_left = max(0, time_limit - int(time.time() - start_time))
        display_timer(time_left, SCREEN_WIDTH - 200, 20)
        
        pygame.display.update()

        # Check events for user input
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if player_input.lower() == word.lower():
                        correct = True  # Correct answer
                    else:
                        display_text(f"Oops! Try again.", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 80, RED, font_type=title_font)
                        pygame.display.update()
                        pygame.time.wait(1000)  # Wait for 1 second before repeating the question
                        # Reset the timer and player input for the next attempt
                        player_input = ""
                        start_time = time.time()
                elif event.key == pygame.K_BACKSPACE:
                    player_input = player_input[:-1]
                else:
                    player_input += event.unicode

        # If time is up, end the question and move to the next one
        if time_left == 0:
            display_text(f"Time's up! The correct answer was: {word}", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 80, RED, font_type=title_font)
            pygame.display.update()
            pygame.time.wait(1000)  # Wait for 1 second before moving to the next question
            player_input = ""  # Reset the player input for the next question
            start_time = time.time()  # Restart the timer

    return True  # Answer is correct, move to next question

# Main game loop
def game():
    global score, level

    # Game loop for all levels
    for current_level in range(1, total_levels + 1):
        screen.fill(BLACK)
        display_text(f"Level {current_level}", 20, 20, LIGHT_BLUE, font_type=title_font)
        pygame.display.update()
        pygame.time.wait(1000)  # Wait for 1 second

        # Generate random questions for this level (6 questions per level)
        for _ in range(6):  # 6 questions per level
            # Randomly select from categories (countries, fruits, vegetables)
            category_choice = random.choice(['countries', 'fruits', 'vegetables'])
            if category_choice == 'countries':
                word = random.choice(countries)
            elif category_choice == 'fruits':
                word = random.choice(fruits)
            elif category_choice == 'vegetables':
                word = random.choice(vegetables)

            scrambled_word = scramble_word(word)

            # Ask the question and check the answer
            correct = ask_question(word, scrambled_word)
            if correct:
                score += 10
                display_text("Correct!", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 80, GREEN, font_type=title_font)
            pygame.display.update()
            pygame.time.wait(1000)  # Wait for 1 second before next question
        # Level completed
        display_text(f"Level {current_level} Completed!", SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2 + 80, LIGHT_GREEN, font_type=title_font)
        pygame.display.update()
        pygame.time.wait(2000)  # Wait for 2 seconds before moving to the next level
    pygame.quit()

# Run the game
game()