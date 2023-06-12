import random

from connect4_board import Connect4Board
from connect4_game import load_tree

import pygame

# Inicjalizacja Pygame
pygame.init()

# Ustawienia planszy
width = 700
height = 600
row_count = 6
col_count = 7
circle_radius = 50
circle_color = (255, 255, 255)
player1_color = (255, 0, 0)
player2_color = (255, 255, 0)

screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Connect 4")


def draw_board(board):
    for row in range(row_count):
        for col in range(col_count):
            pygame.draw.circle(screen, circle_color, (col * 100 + 50, row * 100 + 100), circle_radius)
            if board[row][col] == 0:
                pygame.draw.circle(screen, player1_color, (col * 100 + 50, row * 100 + 100), circle_radius - 5)
            elif board[row][col] == 1:
                pygame.draw.circle(screen, player2_color, (col * 100 + 50, row * 100 + 100), circle_radius - 5)



def play_vs_ai():
    tree = load_tree(f"MCTS_10m_6_7_100.pkl")
    board = Connect4Board.create_empty_board(6, 7)
    def refresh():
        screen.fill((0,0,0))
        draw_board(board.board)
        pygame.display.flip()

    player_turn = bool(random.getrandbits(1))
    while True:
        while player_turn:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    col = event.pos[0] // 100
                    if 0 <= col < col_count:
                        board.make_move(col)
                        player_turn = False
        # row = int(input("Enter row: "))
        # board = board.make_move(row)
        # print(board.board)
        refresh()
        if board.terminal:
            break

        for _ in range(100):
            tree.playout(board)
        board: Connect4Board = tree.choose(board)
        player_turn = True
        # print()
        # print(board.board)
        refresh()
        if board.terminal:
            break
    print("Game ended:")
    print(board.board)

play_vs_ai()

pygame.quit()
