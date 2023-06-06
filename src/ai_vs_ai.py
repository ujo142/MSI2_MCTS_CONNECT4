from connect4 import Connect4
from game_finished_checker import COMPUTER, HUMAN



def play_ai_vs_ai():
    c4 = Connect4()
    c4.print_board()
    while True:
        c4.make_mcts_move(HUMAN)
        c4.make_mcts_move(COMPUTER)


if __name__ == '__main__':
    c4 = Connect4()
    play_ai_vs_ai()
