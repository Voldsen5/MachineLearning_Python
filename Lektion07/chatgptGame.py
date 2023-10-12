import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 300, 300
LINE_WIDTH = 15
WHITE = (255, 255, 255)
LINE_COLOR = (0, 0, 0)
GRID_SIZE = 3
SQUARE_SIZE = WIDTH // GRID_SIZE

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")

# Initialize game variables
board = [['' for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
player_turn = 'X'
game_over = False
winner = None

# Function to draw the grid
def draw_grid():
    for row in range(1, GRID_SIZE):
        pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE), (WIDTH, row * SQUARE_SIZE), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (row * SQUARE_SIZE, 0), (row * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Function to draw X and O
def draw_xo():
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            if board[row][col] == 'X':
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, row * SQUARE_SIZE), ((col + 1) * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), LINE_WIDTH)
                pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE, (row + 1) * SQUARE_SIZE), ((col + 1) * SQUARE_SIZE, row * SQUARE_SIZE), LINE_WIDTH)
            elif board[row][col] == 'O':
                pygame.draw.circle(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - LINE_WIDTH)

# Function to check for a win
def check_win():
    global winner
    for row in range(GRID_SIZE):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != '':
            winner = board[row][0]
            pygame.draw.line(screen, LINE_COLOR, (0, row * SQUARE_SIZE + SQUARE_SIZE // 2), (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)
            return True
    for col in range(GRID_SIZE):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != '':
            winner = board[0][col]
            pygame.draw.line(screen, LINE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT), LINE_WIDTH)
            return True
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != '':
        winner = board[0][0]
        pygame.draw.line(screen, LINE_COLOR, (0, 0), (WIDTH, HEIGHT), LINE_WIDTH)
        return True
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != '':
        winner = board[0][2]
        pygame.draw.line(screen, LINE_COLOR, (0, HEIGHT), (WIDTH, 0), LINE_WIDTH)
        return True
    return False

# Main game loop
while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if not game_over and winner is None:
            if event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]:
                x, y = event.pos
                col = x // SQUARE_SIZE
                row = y // SQUARE_SIZE
                if board[row][col] == '':
                    board[row][col] = player_turn
                    if player_turn == 'X':
                        player_turn = 'O'
                    else:
                        player_turn = 'X'
                    if check_win():
                        game_over = True
                    elif all(board[i][j] != '' for i in range(GRID_SIZE) for j in range(GRID_SIZE)):
                        game_over = True

    # Clear the screen
    screen.fill(WHITE)

    # Draw the grid
    draw_grid()

    # Draw X and O
    draw_xo()

    # Update the display
    pygame.display.update()

# Display the winner or a draw message
font = pygame.font.Font(None, 36)
if winner:
    text = f"Player {winner} wins!"
else:
    text = "It's a draw!"
text_surface = font.render(text, True, LINE_COLOR)
text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
screen.blit(text_surface, text_rect)
pygame.display.update()

# Wait for a moment and then quit
pygame.time.wait(2000)
pygame.quit()
sys.exit()
