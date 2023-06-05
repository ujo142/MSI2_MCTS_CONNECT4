from connect4 import Connect4
from game_finished_checker import COMPUTER
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

# Wczytanie obrazu tła
background_image = pygame.image.load('./images/radek.png')
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Funkcja do rysowania planszy
def draw_board():
    # Rysowanie tła
    screen.blit(background_image, (0, 0))

    for row in range(ROWS):
        for col in range(COLS):
            # Obliczenie pozycji kółka
            circle_x = board_x + col * SQUARE_SIZE + SQUARE_SIZE // 2
            circle_y = board_y + (row + 1) * SQUARE_SIZE + SQUARE_SIZE // 2

            # Pobranie koloru tła
            bg_color = background_image.get_at((circle_x, circle_y))

            # Rysowanie obramówki kółka
            pygame.draw.circle(screen, BLUE, (circle_x, circle_y), SQUARE_SIZE // 2, 5)

            # Ustawienie przezroczystości wewnątrz kółka
            circle_surface = pygame.Surface((SQUARE_SIZE, SQUARE_SIZE), pygame.SRCALPHA)
            circle_color = (*bg_color[:3], 128)
            pygame.draw.circle(circle_surface, circle_color, (SQUARE_SIZE // 2, SQUARE_SIZE // 2), SQUARE_SIZE // 2 - 5)

            # Wyświetlanie przezroczystego kółka na ekranie
            screen.blit(circle_surface, (circle_x - SQUARE_SIZE // 2, circle_y - SQUARE_SIZE // 2))

# Funkcja do zwracania indeksu klikniętej kolumny
def get_clicked_column(x):
    return (x - board_x) // SQUARE_SIZE

def read_input(team):
    col = None
    while col is None:
        try:
            i = int(input(team + ": Enter the number of column:"))
            if 0 <= i <= 6:
                col = i

        except KeyboardInterrupt:
            raise
        except:
            continue
    return col

def play_with_computer():
    # Rysowanie planszy
    screen.blit(background_image, (0, 0))
    draw_board()
    pygame.display.update()
    
    # glowa petla programu
    while True:
        # Sprawdzenie zdarzeń
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Pobranie pozycji kliknięcia myszą
                x, y = event.pos
               
                # Sprawdzenie, czy kliknięcie jest na planszy
                if board_x <= x <= board_x + board_width and board_y <= y <= board_y + board_height:
                    # pobranie kolumny z klikniecia
                    col = get_clicked_column(x)
                
                    # zrob ruch czlowieka
                    c4.red_move(col)
                    
                    # pobierz ostatni ruch
                    x, y = c4.last_move
                    
                    # Obliczenie współrzędnych dla rysowania kółka wewnątrz planszy
                    circle_x = board_x  + SQUARE_SIZE // 2 + y * SQUARE_SIZE
                    circle_y = board_y + (ROWS - x + 1) * SQUARE_SIZE - SQUARE_SIZE // 2
                    
                    # Rysowanie kółka
                    pygame.draw.circle(screen, RED, (circle_x, circle_y), SQUARE_SIZE // 2 - 5)

                    # Aktualizacja ekranu
                    pygame.display.update()
                    
                # ruch AI
                c4.make_mcts_move(COMPUTER)
                
                # pobierz wspolrzedne ostatniego ruchu
                x, y = c4.last_move
         
                # Obliczenie współrzędnych dla rysowania kółka wewnątrz planszy
                circle_x = board_x  + SQUARE_SIZE // 2 + y * SQUARE_SIZE
                circle_y = board_y + (ROWS - x + 1) * SQUARE_SIZE - SQUARE_SIZE // 2

                # Rysowanie kółka
                pygame.draw.circle(screen, YELLOW, (circle_x, circle_y), SQUARE_SIZE // 2 - 5)

                # Aktualizacja ekranu
                pygame.display.update()      

def multiplayer():
    c4.print_board()
    while True:
        col = read_input("RED")
        c4.red_move(col)
        col = read_input("BLUE")
        c4.blue_move(col)


if __name__ == '__main__':
    c4 = Connect4()
    play_with_computer()
