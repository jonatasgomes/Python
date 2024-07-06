import os
import random
import time


class TicTacToe:
    def __init__(self):
        self.positions = {f'{i},{j}': ' ' for i in range(1, 4) for j in range(1, 4)}
        self.scores = {'h': 0, 'c': 0}
        self.turn = ''
        self.move = ''
        self.winner = ''

    def restart_game(self):
        self.positions = {key: ' ' for key in self.positions}
        self.turn = ''

    def is_move_valid(self, move):
        return move in self.positions and self.positions[move] == ' '

    def is_game_finished(self):
        lines = [
            ['1,1', '1,2', '1,3'], ['2,1', '2,2', '2,3'], ['3,1', '3,2', '3,3'],
            ['1,1', '2,1', '3,1'], ['1,2', '2,2', '3,2'], ['1,3', '2,3', '3,3'],
            ['1,1', '2,2', '3,3'], ['1,3', '2,2', '3,1']
        ]
        for line in lines:
            if self.positions[line[0]] == self.positions[line[1]] == self.positions[line[2]] != ' ':
                self.winner = self.turn
                return True
        if ' ' not in self.positions.values():
            self.winner = 'd'
            return True
        return False

    def check_move(self):
        if self.move in ['n', 'q']:
            return
        if self.is_move_valid(self.move):
            self.positions[self.move] = "X" if self.turn == 'h' else "O"
            if self.is_game_finished():
                self.scores[self.turn] += 1
                self.turn = 'd'
            else:
                self.turn = 'c' if self.turn == 'h' else 'h'
        else:
            input('Invalid move! Press enter to try again...')

    def computer_move(self):
        time.sleep(1)
        while True:
            move = f'{random.randint(1, 3)},{random.randint(1, 3)}'
            if self.is_move_valid(move):
                self.move = move
                break
        print(self.move)
        time.sleep(1)

    def display_board(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print('==============================')
        print('Welcome to Tic-Tac-Toe!')
        print(f'Human: {self.scores["h"]} | Computer: {self.scores["c"]}')
        print('==============================')
        for i in range(1, 4):
            print(' | '.join(self.positions[f'{i},{j}'] for j in range(1, 4)))
            if i < 3:
                print('-----------')

    def start_game(self):
        while True:
            self.display_board()
            if self.turn == '':
                self.turn = input('Who goes first? h (human) or c (computer) or q (quit): ').strip()
                if self.turn == 'q':
                    break
                elif self.turn not in ['h', 'c']:
                    self.turn = ''
                    input('Invalid option! Press enter to continue...')
            if self.turn == 'd':
                if self.winner in ['h', 'c']:
                    print(f'{"Human" if self.winner == "h" else "Computer"} wins!')
                elif self.winner == 'd':
                    print('It is a draw!')
                self.turn = input('n (new game) or q (quit): ').strip()
                if self.turn not in ['n', 'q']:
                    self.turn = 'd'
                    input('Invalid option! Press enter to continue...')
            if self.turn in ['h', 'c']:
                if self.turn == 'h':
                    self.move = input(
                        'Human, what is the move? row,column or n (new game) or q (quit): ').strip().replace(' ', '')
                elif self.turn == 'c':
                    print('Computer, what is the move? row,column or n (new game) or q (quit): ', end='')
                    self.computer_move()
                self.check_move()
            if self.turn == 'n' or self.move == 'n':
                self.restart_game()
            if self.turn == 'q' or self.move == 'q':
                break


if __name__ == "__main__":
    game = TicTacToe()
    game.start_game()
