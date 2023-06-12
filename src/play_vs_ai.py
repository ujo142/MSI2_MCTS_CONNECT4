import random
import time

from connect4_board import Connect4Board
import PySimpleGUI as sg

from config import Config
from MCTS import MCTS
from MCTS_puct import MCTS_PUCT
from MCTS_rave import MCTS_RAVE
from heuristics import PotentialSeriesHeuristic, CentralHeuristic

config = Config()
trees = [MCTS(config, int(time.time()), heuristic=PotentialSeriesHeuristic()), MCTS_RAVE(config, int(time.time()), heuristic=PotentialSeriesHeuristic()),  MCTS_PUCT(config, int(time.time()), heuristic=PotentialSeriesHeuristic()), MCTS(config, int(time.time()), heuristic=CentralHeuristic()), MCTS_RAVE(config, int(time.time()), heuristic=CentralHeuristic()),  MCTS_PUCT(config, int(time.time()), heuristic=CentralHeuristic()), MCTS(config, int(time.time())), MCTS_RAVE(config, int(time.time())),  MCTS_PUCT(config, int(time.time()))]

# Ustawienia planszy
board = [[5 for _ in range(7)] for _ in range(6)]
circle_colors = ["yellow", "red", "", "", "","black"]

# Definicja layoutu
layout = []
for row in range(6):
    row_layout = []
    for col in range(7):
        circle = sg.Button(button_text="   ", size=(3, 1), key=(row, col))
        row_layout.append(circle)

    layout.append(row_layout)

# Tworzenie okna
window = sg.Window("Connect 4", layout, finalize=True)

def handle_click(board, col, player):
    for row in range(5, -1, -1):
        if board[row][col] == 5:
            board[row][col] = player
            window[(row, col)].update(button_color=('black', circle_colors[player]))
            break


def draw_board(board):
    for row in range(6):
        for col in range(7):
            player = board[row][col]
            window[(row, col)].update(button_color=('black', circle_colors[player]))




def play_vs_ai():
    tree = MCTS(config, int(time.time()))
    board = Connect4Board.create_empty_board(6, 7)
    draw_board(board.board)

    player_turn = bool(random.getrandbits(1))
    player_checker = 0
    while True:
        while player_turn:
            event, values = window.read()
            if event == sg.WINDOW_CLOSED:
                return
            col = event[1]
            handle_click(board.board, col, player_checker)
            player_turn=False
            draw_board(board.board)
        # row = int(input("Enter row: "))
        # board = board.make_move(row)
        # print(board.board)
        if board.terminal:
            break

        board: Connect4Board = tree.make_move(board)
        player_turn = True
        # print()
        # print(board.board)
        draw_board(board.board)
        if board.terminal:
            break
    winner = board.winner
    if winner == 0:
        winner = "human won"
    elif winner == 1:
        winner = "bot won"
    else:
        winner = "draw"
    print("Game ended: " + winner)
    print(board.board)

play_vs_ai()

window.close()
