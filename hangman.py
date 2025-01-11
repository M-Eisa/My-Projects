import pygame
import random

# Initialize Pygame
pygame.init()

# Game settings
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 400
MAX_ATTEMPTS = 6  # Number of incorrect guesses before the game is over

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (200, 200, 200)

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Hangman")

# List of words for the game
words = [
    "beginning", "words", "bizarre", "climate", "dolphin", "eclipse", "fluctuate", "giraffe", "harmony", "incredible",
    "jungle", "kangaroo", "lighthouse", "mountain", "nebulous", "obstacle", "chalk", "piano", "radiator", "tennis",
    "mercy", "tornado", "underestimate", "vibrant", "whistle", "abstract", "yellow", "zebra", "tracker", "bicycle",
    "crystal", "donkey", "light", "fate", "glimpse", "snake", "inspire", "flames", "keynote", "lullaby", "majestic",
    "nurture", "octopus", "permanent", "amazing", "resilient", "serenity", "tangible", "universe", "vivid", "wonder",
    "phobia", "yield", "website", "articulate", "backbone", "cipher", "diverse", "ellipse", "fascinate", "grit",
    "height", "scaffolding", "joker", "knead", "curious", "miracle", "nullify", "opinion", "puncture", "touring",
    "pizza", "subtle", "library", "bottle", "vulnerable", "tired", "exit", "yacht", "jealous", "affiliate", "bizarre",
    "circumstance", "trust", "currency", "question", "harmony", "examination", "juggle", "keen", "livid", "current",
    "noble", "overcome", "pretentious", "deck", "riddle", "stumble", "threshold", "utilize", "vacuum", "curtain",
    "person", "security", "tough", "simple", "basket", "courage", "detour", "engage", "fragile", "keyboard", "harvest",
    "impose", "jungle", "knight", "learn", "moody", "laptop", "obscure", "pale", "thrive", "sharpener", "system",
    "complicated", "ultimatum", "variety", "whistle", "extra", "charger", "zoom", "adore", "something", "chuckle",
    "delight", "entice", "drip", "exhaust", "headphones", "irrational", "species", "karma", "surprised", "password",
    "naive", "obligate", "screening", "shiver", "middle", "vehicle", "taunt", "undermine", "vile", "wary", "scramble",
    "telephone", "zone", "arbitrary", "frozen", "addition", "sanitizer", "project", "manager", "exit", "trivial",
    "marshmallow", "royal", "vector", "airplane", "wristwatch", "cheetah", "typewriter", "snail", "blackboard",
    "pothole", "asphalt", "wallet", "money", "scale", "textbook", "declaration", "setting", "script", "outlet",
    "jacket", "delete", "page", "eagle", "eraser", "play", "print", "column", "command", "expense", "logical",
    "font", "paper", "sign", "illustration", "spine", "muffler", "construction", "degrade", "community", "weather",
    "bright", "hang", "answer", "solution", "interesting", "exaggeration", "shirt", "turbulence", "definition",
    "explanation", "train", "workout", "gym", "example", "puzzle", "theatre", "movie", "square", "tactical", "domino",
    "hands", "finished"
]


# Font settings
font = pygame.font.SysFont(None, 40)
big_font = pygame.font.SysFont(None, 70)

# Define the game logic
class HangmanGame:
    def __init__(self, difficulty):
        self.word = self.get_word(difficulty)
        self.guessed_letters = []
        self.incorrect_guesses = 0
        self.display_word = ["_"] * len(self.word)

    def get_word(self, difficulty):
        if difficulty == "Easy":
            return random.choice([word for word in words if len(word) <= 4])
        elif difficulty == "Medium":
            return random.choice([word for word in words if 5 <= len(word) <= 7])
        elif difficulty == "Hard":
            return random.choice([word for word in words if len(word) >= 8])

    def guess(self, letter):
        if letter in self.guessed_letters:
            return False
        self.guessed_letters.append(letter)
        if letter in self.word:
            for i in range(len(self.word)):
                if self.word[i] == letter:
                    self.display_word[i] = letter
            return True
        else:
            self.incorrect_guesses += 1
            return False

    def use_hint(self):
        for i, letter in enumerate(self.word):
            if self.display_word[i] == "_":
                self.display_word[i] = letter
                self.guessed_letters.append(letter)
                break

    def is_game_over(self):
        return self.incorrect_guesses >= MAX_ATTEMPTS or "_" not in self.display_word

    def is_winner(self):
        return "_" not in self.display_word

# Function to draw the hangman at each stage
def draw_hangman(stage):
    pygame.draw.line(screen, BLACK, (150, 350), (450, 350), 5)
    pygame.draw.line(screen, BLACK, (200, 350), (200, 50), 5)
    pygame.draw.line(screen, BLACK, (200, 50), (350, 50), 5)
    pygame.draw.line(screen, BLACK, (350, 50), (350, 100), 5)

    if stage >= 1:  # Head
        pygame.draw.circle(screen, BLACK, (350, 150), 40, 2)
    if stage >= 2:  # Body
        pygame.draw.line(screen, BLACK, (350, 190), (350, 250), 2)
    if stage >= 3:  # Left arm
        pygame.draw.line(screen, BLACK, (350, 210), (300, 230), 2)
    if stage >= 4:  # Right arm
        pygame.draw.line(screen, BLACK, (350, 210), (400, 230), 2)
    if stage >= 5:  # Left leg
        pygame.draw.line(screen, BLACK, (350, 250), (300, 300), 2)
    if stage >= 6:  # Right leg
        pygame.draw.line(screen, BLACK, (350, 250), (400, 300), 2)

# Function to display text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

# Function for the difficulty selection screen
def select_difficulty():
    running = True
    difficulty = None
    while running:
        screen.fill(WHITE)
        draw_text("Select Difficulty", big_font, BLACK, SCREEN_WIDTH // 2 - 175, 50)

        easy_button = pygame.draw.rect(screen, GREEN, (150, 150, 200, 100))
        medium_button = pygame.draw.rect(screen, BLUE, (400, 150, 200, 100))
        hard_button = pygame.draw.rect(screen, RED, (650, 150, 200, 100))

        draw_text("Easy", font, WHITE, 221, 190)
        draw_text("Medium", font, WHITE, 450, 190)
        draw_text("Hard", font, WHITE, 720, 190)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                if easy_button.collidepoint(mouse_pos):
                    difficulty = "Easy"
                    running = False
                elif medium_button.collidepoint(mouse_pos):
                    difficulty = "Medium"
                    running = False
                elif hard_button.collidepoint(mouse_pos):
                    difficulty = "Hard"
                    running = False

        pygame.display.flip()
    return difficulty


def end_screen(game):
    running = True
    while running:
        screen.fill(WHITE)
        if game.is_winner():
            draw_text("You Win!", big_font, GREEN, 400, 150)
        else:
            draw_text("You Lose!", big_font, RED, 400, 150)
            draw_text(f"The word was: {game.word}", font, BLACK, 400, 200)

        draw_text("Press R to Restart or Q to Quit", font, BLACK, 300, 300)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                elif event.key == pygame.K_q:
                    return False

        pygame.display.flip()

# Main Game Loop
def main():
    while True:
        difficulty = select_difficulty()
        game = HangmanGame(difficulty)
        running = True

        while running:
            screen.fill(WHITE)
            draw_hangman(game.incorrect_guesses)
            draw_text(" ".join(game.display_word), big_font, BLACK, 450, 50)
            draw_text("Guessed Letters: " + ", ".join(game.guessed_letters), font, BLACK, 450, 150)
            draw_text(f"Remaining Attempts: {MAX_ATTEMPTS - game.incorrect_guesses}", font, BLACK, 450, 200)

            hint_button = pygame.draw.rect(screen, GRAY, (650, 300, 150, 50))
            draw_text("Hint", font, WHITE, 700, 312)

            if game.is_game_over():
                running = False

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()
                elif event.type == pygame.KEYDOWN:
                    letter = pygame.key.name(event.key).lower()
                    if len(letter) == 1 and letter.isalpha():
                        game.guess(letter)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if hint_button.collidepoint(event.pos):
                        game.use_hint()

            pygame.display.flip()

        if not end_screen(game):
            break

if __name__ == "__main__":
    main()
    pygame.quit()
