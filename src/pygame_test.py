import pygame

# Inicjalizacja Pygame
pygame.init()

# Ustalenie szerokości i wysokości planszy
WIDTH = 920
HEIGHT = 640

# Ustalenie kolorów
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

# Ustalenie rozmiaru planszy
ROWS = 6
COLS = 7
SQUARE_SIZE = 80

# Obliczenie szerokości i wysokości planszy
board_width = COLS * SQUARE_SIZE
board_height = (ROWS + 1) * SQUARE_SIZE

# Obliczenie pozycji planszy na ekranie
board_x = (WIDTH - board_width) // 2
board_y = (HEIGHT - board_height) // 2

# Utworzenie powierzchni ekranu
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Connect Four")

# Funkcja do rysowania planszy
def draw_board():
    for row in range(ROWS):
        for col in range(COLS):
            pygame.draw.rect(screen, BLUE, (board_x + col * SQUARE_SIZE, board_y + (row + 1) * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, BLACK, (board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2, board_y + (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

# Funkcja do zwracania indeksu klikniętej kolumny
def get_clicked_column(x):
    return (x - board_x) // SQUARE_SIZE

# Funkcja główna gry
def play_game():
    # Pętla główna programu
    running = True
    while running:
        # Sprawdzenie zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pobranie pozycji kliknięcia myszą
                x, y = event.pos
                
                # Sprawdzenie, czy kliknięcie jest na planszy
                if board_x <= x <= board_x + board_width and board_y <= y <= board_y + board_height:
                    col = get_clicked_column(x)
                    print("Clicked column:", col)

        # Wypełnienie ekranu kolorem
        screen.fill(BLACK)

        # Rysowanie planszy
        draw_board()

        # Rysowanie marginesu od dołu planszy
        pygame.draw.rect(screen, BLACK, (0, board_y + (ROWS + 1) * SQUARE_SIZE, WIDTH, HEIGHT - (board_y + (ROWS + 1) * SQUARE_SIZE)))

        # Aktualizacja ekranu
        pygame.display.update()

# Wywołanie funkcji głównej gry
play_game()

# Zamknięcie Pygame
pygame.quit()

"""

while (True):
    # wyswietlenie planszy
    
    # pobranie ruchu od gracza
    
    # sprawdzenie czy ruch jest poprawny
    
    # wykonanie ruchu
    
    # Wyswielenie planszy
    
    # sprawdzenie czy gra sie skonczyla
    
    # ruch AI
    
    # wyswietlenie planszy
"""