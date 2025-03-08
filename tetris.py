import pygame
import random

colors = [
    (0, 0, 0),
    (120, 37, 179),  # Purple
    (100, 179, 179), # Cyan
    (80, 34, 22),    # Brown
    (80, 134, 22),   # Green
    (180, 34, 22),   # Red
    (180, 34, 122),  # Pink
]


class Tetromino:
    x = 0
    y = 0

    # Define all tetromino shapes with their rotations
    tetrominos = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # I
        [[4, 5, 9, 10], [2, 6, 5, 9]],  # Z
        [[6, 7, 9, 10], [1, 5, 6, 10]], # S
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # J
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]], # L
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],    # T
        [[1, 2, 5, 6]],  # O (cube)
    ]

    # Names for the tetrominos
    tetromino_names = ["I", "Z", "S", "J", "L", "T", "O"]

    bounding_boxes = {
        0: {  # I piece
            0: (1, 1, 0, 3),  # vertical orientation
            1: (0, 3, 1, 1)   # horizontal orientation
        },
        1: {  # Z piece
            0: (0, 2, 1, 2),
            1: (1, 2, 0, 2)
        },
        2: {  # S piece
            0: (0, 2, 1, 2),
            1: (1, 2, 0, 2)
        },
        3: {  # J piece
            0: (1, 2, 0, 2),
            1: (0, 2, 0, 1),
            2: (0, 1, 0, 2),
            3: (0, 2, 1, 2)
        },
        4: {  # L piece
            0: (1, 2, 0, 2),
            1: (0, 2, 1, 2),
            2: (1, 2, 0, 2),
            3: (0, 2, 0, 1)
        },
        5: {  # T piece
            0: (0, 2, 1, 1),
            1: (1, 1, 0, 2),
            2: (0, 2, 1, 1),
            3: (1, 1, 0, 2)
        },
        6: {  # O piece
            0: (1, 2, 1, 2)
        }
    }

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.type = random.randint(0, len(self.tetrominos) - 1)
        self.color = random.randint(1, len(colors) - 1)
        self.rotation = 0

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.tetrominos[self.type])

    def image(self):
        return self.tetrominos[self.type][self.rotation]

    def name(self):
        return self.tetromino_names[self.type]

    def get_bounding_box(self):
        """Return the bounding box for the current tetromino shape"""
        return self.bounding_boxes[self.type][self.rotation]


class Tetris:
    def __init__(self, height, width):
        self.level = 1
        self.score = 0
        self.state = "start"
        self.field = []
        self.height = 0
        self.width = 0
        self.x = 100
        self.y = 60
        self.zoom = 20
        self.tetromino = None
        self.next_tetromino = None
        self.paused = False
        self.total_lines = 0
        self.high_score = self.load_high_score()
        self.ghost_piece = True
        self.hold_piece = None
        self.can_hold = True
        self.game_started = False
        self.combo_count = 0

        # Difficulty settings
        self.height = height
        self.width = width
        self.field = []
        for i in range(height):
            new_line = []
            for j in range(width):
                new_line.append(0)
            self.field.append(new_line)

    def new_tetromino(self):
        if self.next_tetromino is None:
            self.tetromino = Tetromino(3, 0)
            self.next_tetromino = Tetromino(3, 0)
        else:
            self.tetromino = self.next_tetromino
            self.next_tetromino = Tetromino(3, 0)

        self.game_started = True

    def hold_current_piece(self):
        if not self.can_hold:
            return

        if self.hold_piece is None:
            # First hold - just store current piece and get next one
            self.hold_piece = Tetromino(0, 0)
            self.hold_piece.type = self.tetromino.type
            self.hold_piece.color = self.tetromino.color
            self.hold_piece.rotation = 0  # Reset rotation when holding

            # Get the next piece
            self.tetromino = self.next_tetromino
            self.next_tetromino = Tetromino(3, 0)
        else:
            # Swap current piece with held piece
            temp_type = self.tetromino.type
            temp_color = self.tetromino.color

            self.tetromino.type = self.hold_piece.type
            self.tetromino.color = self.hold_piece.color
            self.tetromino.rotation = 0  # Reset rotation
            self.tetromino.x = 3  # Reset position
            self.tetromino.y = 0

            self.hold_piece.type = temp_type
            self.hold_piece.color = temp_color

        self.can_hold = False  # Can't hold again until next piece

    def get_ghost_position(self):
        """Calculate where the current piece would land if dropped"""
        if self.tetromino is None:
            return None

        # Create a copy of current position
        ghost_y = self.tetromino.y

        # Move down until collision
        while True:
            ghost_y += 1
            # Check if this position would intersect
            if self._would_intersect(self.tetromino.x, ghost_y, self.tetromino.rotation):
                ghost_y -= 1  # Move back up to last valid position
                break

        return ghost_y

    def _would_intersect(self, x, y, rotation):
        """Check if the tetromino would intersect at given position and rotation"""
        current_rotation = self.tetromino.rotation
        current_x = self.tetromino.x
        current_y = self.tetromino.y

        # Temporarily move piece to check position
        self.tetromino.x = x
        self.tetromino.y = y
        self.tetromino.rotation = rotation

        # Check intersection
        result = self.intersects()

        # Restore original position
        self.tetromino.x = current_x
        self.tetromino.y = current_y
        self.tetromino.rotation = current_rotation

        return result

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetromino.image():
                    if i + self.tetromino.y > self.height - 1 or \
                            j + self.tetromino.x > self.width - 1 or \
                            j + self.tetromino.x < 0 or \
                            self.field[i + self.tetromino.y][j + self.tetromino.x] > 0:
                        intersection = True
        return intersection

    def break_lines(self):
        lines = 0
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                lines += 1
                for i1 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i1][j] = self.field[i1 - 1][j]

        # Update the score based on the number of lines cleared
        if lines > 0:
            self.total_lines += lines
            # Level up every 10 lines
            self.level = min(20, self.total_lines // 10 + 1)  # Cap level at 20

            # Update combo counter
            self.combo_count += 1
            combo_bonus = (self.combo_count - 1) * 50 if self.combo_count > 1 else 0

            # Score calculation: more points for clearing multiple lines at once
            line_scores = [0, 100, 300, 700, 1500]  # 0, 1, 2, 3, or 4 lines
            self.score += (line_scores[min(lines, 4)] * self.level) + combo_bonus

            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()
        else:
            # Reset combo if no lines cleared
            self.combo_count = 0

    def load_high_score(self):
        try:
            with open("tetris_high_score.txt", "r") as f:
                return int(f.read())
        except:
            return 0

    def save_high_score(self):
        try:
            with open("tetris_high_score.txt", "w") as f:
                f.write(str(self.high_score))
        except:
            pass

    def go_space(self):
        while not self.intersects():
            self.tetromino.y += 1
        self.tetromino.y -= 1
        self.freeze()

    def go_down(self):
        self.tetromino.y += 1
        if self.intersects():
            self.tetromino.y -= 1
            self.freeze()

    def freeze(self):
        for i in range(4):
            for j in range(4):
                if i * 4 + j in self.tetromino.image():
                    self.field[i + self.tetromino.y][j + self.tetromino.x] = self.tetromino.color
        self.break_lines()
        self.new_tetromino()
        self.can_hold = True  # Reset hold ability
        if self.intersects():
            self.state = "gameover"
            # Check if this is a new high score
            if self.score > self.high_score:
                self.high_score = self.score
                self.save_high_score()

    def go_side(self, dx):
        old_x = self.tetromino.x
        self.tetromino.x += dx
        if self.intersects():
            self.tetromino.x = old_x

    def rotate(self):
        old_rotation = self.tetromino.rotation
        self.tetromino.rotate()
        if self.intersects():
            # Try wall kicks - nudge left, right, and up if rotation causes collision
            for kick_x in [-1, 1, 0]:
                for kick_y in [0, -1]:
                    if kick_x == 0 and kick_y == 0:
                        continue

                    self.tetromino.x += kick_x
                    self.tetromino.y += kick_y

                    if not self.intersects():
                        return  # Found a valid position

                    # Revert the kick attempt
                    self.tetromino.x -= kick_x
                    self.tetromino.y -= kick_y

            # If all kick attempts failed, revert rotation
            self.tetromino.rotation = old_rotation

    def toggle_pause(self):
        self.paused = not self.paused

    def toggle_ghost(self):
        self.ghost_piece = not self.ghost_piece


# Initialize the game engine
pygame.init()

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
DARK_BLUE = (44, 44, 127)
LIGHT_BLUE = (173, 216, 230)
GHOST_COLOR = (210, 210, 210)  # Light gray for ghost piece

# Game window size
size = (600, 600)  # Make window wider to fit hold piece
screen = pygame.display.set_mode(size)

pygame.display.set_caption("Tetris")

# Game help text
help_text = [
    "Controls:",
    "← → : Move left/right",
    "↑ : Rotate",
    "↓ : Move down",
    "SPACE : Drop",
    "C : Hold piece",
    "G : Toggle ghost",
    "P : Pause",
    "ESC : New game"
]

# Draw grid function
def draw_grid(game, screen):
    for i in range(game.height):
        for j in range(game.width):
            pygame.draw.rect(screen, GRAY,
                             [game.x + game.zoom * j, game.y + game.zoom * i, game.zoom, game.zoom], 1)
            if game.field[i][j] > 0:
                pygame.draw.rect(screen, colors[game.field[i][j]],
                                 [game.x + game.zoom * j + 1, game.y + game.zoom * i + 1,
                                  game.zoom - 2, game.zoom - 1])

# Draw current tetromino
def draw_tetromino(tetromino, x, y, zoom, screen):
    if tetromino is not None:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in tetromino.image():
                    pygame.draw.rect(screen, colors[tetromino.color],
                                     [x + zoom * (j + tetromino.x) + 1,
                                      y + zoom * (i + tetromino.y) + 1,
                                      zoom - 2, zoom - 2])

# Draw ghost piece (shows where piece will land)
def draw_ghost_piece(game, screen, ghost_y):
    if game.tetromino is not None and game.ghost_piece:
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in game.tetromino.image():
                    pygame.draw.rect(screen, GHOST_COLOR,
                                     [game.x + game.zoom * (j + game.tetromino.x) + 1,
                                      game.y + game.zoom * (i + ghost_y) + 1,
                                      game.zoom - 2, game.zoom - 2], 1)  # Outline only

# Draw piece in preview/hold area, centered
def draw_preview_piece(tetromino, x, y, zoom, screen, is_hold=False):
    if tetromino is not None:
        # Get the bounding box to calculate centering offsets
        min_x, max_x, min_y, max_y = tetromino.get_bounding_box()

        # Calculate width and height of this tetromino
        width = max_x - min_x + 1
        height = max_y - min_y + 1

        # Calculate centering offsets
        offset_x = (4 - width) // 2
        offset_y = (4 - height) // 2

        # Draw the piece
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in tetromino.image():
                    pygame.draw.rect(screen, colors[tetromino.color],
                                     [x + zoom * (j + offset_x) + 1,
                                      y + zoom * (i + offset_y) + 1,
                                      zoom - 2, zoom - 2])

# Loop until the user clicks the close button
done = False
clock = pygame.time.Clock()
fps = 25
game = Tetris(20, 10)
counter = 0

pressing_down = False

# Main game loop
while not done:
    # Create a new tetromino if needed
    if game.tetromino is None and game.next_tetromino is None:
        game.new_tetromino()

    counter += 1
    if counter > 100000:
        counter = 0

    # Handle game speed based on level
    if counter % (fps // game.level // 2) == 0 or pressing_down:
        if game.state == "start" and not game.paused:
            game.go_down()

    # Get ghost piece position
    ghost_y = game.get_ghost_position() if game.tetromino and game.ghost_piece else None

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and not game.paused:
                game.rotate()
            if event.key == pygame.K_DOWN and not game.paused:
                pressing_down = True
            if event.key == pygame.K_LEFT and not game.paused:
                game.go_side(-1)
            if event.key == pygame.K_RIGHT and not game.paused:
                game.go_side(1)
            if event.key == pygame.K_SPACE and not game.paused:
                game.go_space()
            if event.key == pygame.K_c and not game.paused:  # Hold piece with C key
                game.hold_current_piece()
            if event.key == pygame.K_g:  # Toggle ghost piece
                game.toggle_ghost()
            if event.key == pygame.K_ESCAPE:
                game.__init__(20, 10)
            if event.key == pygame.K_p:
                game.toggle_pause()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_DOWN:
                pressing_down = False

    # Fill the screen with a light blue background
    screen.fill(LIGHT_BLUE)

    # Draw game area with darker background
    pygame.draw.rect(screen, DARK_BLUE, [game.x, game.y, game.width * game.zoom, game.height * game.zoom])

    # Draw the ghost piece first (so it appears underneath the active piece)
    if ghost_y is not None:
        draw_ghost_piece(game, screen, ghost_y)

    # Draw the grid and active piece
    draw_grid(game, screen)
    draw_tetromino(game.tetromino, game.x, game.y, game.zoom, screen)

    # Draw hold piece area (on the left side)
    hold_x = game.x - 100
    hold_y = game.y + 50
    hold_size = game.zoom * 4

    # Hold area background
    pygame.draw.rect(screen, DARK_BLUE, [hold_x, hold_y, hold_size, hold_size])
    pygame.draw.rect(screen, GRAY, [hold_x, hold_y, hold_size, hold_size], 1)

    # Draw hold piece in hold area
    if game.hold_piece is not None:
        draw_preview_piece(game.hold_piece, hold_x, hold_y, game.zoom, screen, is_hold=True)

    # Draw preview area (on the right side)
    preview_x = game.x + game.width * game.zoom + 20
    preview_y = game.y + 50
    preview_size = game.zoom * 4

    # Preview background
    pygame.draw.rect(screen, DARK_BLUE, [preview_x, preview_y, preview_size, preview_size])
    pygame.draw.rect(screen, GRAY, [preview_x, preview_y, preview_size, preview_size], 1)

    # Draw next piece in preview area
    if game.next_tetromino is not None:
        draw_preview_piece(game.next_tetromino, preview_x, preview_y, game.zoom, screen)

    # Fonts for text
    font = pygame.font.SysFont('Calibri', 25, True, False)
    font_small = pygame.font.SysFont('Calibri', 20, True, False)
    font_big = pygame.font.SysFont('Calibri', 65, True, False)

    # Game information
    text_hold = font.render("Hold:", True, BLACK)
    text_next = font.render("Next:", True, BLACK)
    text_score = font.render("Score: " + str(game.score), True, BLACK)
    text_high_score = font.render("High Score: " + str(game.high_score), True, BLACK)
    text_level = font.render("Level: " + str(game.level), True, BLACK)
    text_lines = font.render("Lines: " + str(game.total_lines), True, BLACK)

    # Combo counter (display only when combo > 1)
    if game.combo_count > 1:
        text_combo = font.render(f"Combo: x{game.combo_count}", True, (255, 0, 0))
        screen.blit(text_combo, [preview_x, preview_y + preview_size + 140])

    # Draw the info text
    screen.blit(text_hold, [hold_x, hold_y - 30])
    screen.blit(text_next, [preview_x, preview_y - 30])
    screen.blit(text_score, [preview_x, preview_y + preview_size + 20])
    screen.blit(text_high_score, [preview_x, preview_y + preview_size + 50])
    screen.blit(text_level, [preview_x, preview_y + preview_size + 80])
    screen.blit(text_lines, [preview_x, preview_y + preview_size + 110])

    # Help text
    y_offset = 370
    for line in help_text:
        text_help = font_small.render(line, True, BLACK)
        screen.blit(text_help, [preview_x, y_offset])
        y_offset += 25

    # Game Over state
    if game.state == "gameover":
        # Semi-transparent overlay
        s = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))  # Darker overlay
        screen.blit(s, (0, 0))

        # Game over text
        screen.blit(font_big.render("Game Over", True, (255, 125, 0)), [120, 200])
        screen.blit(font.render(f"Final Score: {game.score}", True, WHITE), [180, 280])
        screen.blit(font.render("Press ESC for New Game", True, (255, 215, 0)), [150, 320])

    # Paused state
    if game.paused:
        # Semi-transparent overlay
        s = pygame.Surface((size[0], size[1]), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        screen.blit(s, (0, 0))
        screen.blit(font_big.render("PAUSED", True, WHITE), [180, 200])
        screen.blit(font.render("Press P to continue", True, WHITE), [180, 280])

    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
