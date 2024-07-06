import os
import random
import time

positions = {
    '1,1': ' ', '1,2': ' ', '1,3': ' ',
    '2,1': ' ', '2,2': ' ', '2,3': ' ',
    '3,1': ' ', '3,2': ' ', '3,3': ' '
}
scores = {
    'h': 0,
    'c': 0
}
turn = ''
move = ''
winner = ''


def restart_game():
    global turn
    for i in positions.keys():
        positions[i] = ' '
    turn = ''


def is_move_valid():
    if move in positions.keys():
        if positions[move] == ' ':
            return True
    return False


def is_game_finished():
    global winner
    if (positions['1,1'] == positions['1,2'] == positions['1,3'] != ' ') or \
            (positions['2,1'] == positions['2,2'] == positions['2,3'] != ' ') or \
            (positions['3,1'] == positions['3,2'] == positions['3,3'] != ' ') or \
            (positions['1,1'] == positions['2,1'] == positions['3,1'] != ' ') or \
            (positions['1,2'] == positions['2,2'] == positions['3,2'] != ' ') or \
            (positions['1,3'] == positions['2,3'] == positions['3,3'] != ' ') or \
            (positions['1,1'] == positions['2,2'] == positions['3,3'] != ' ') or \
            (positions['1,3'] == positions['2,2'] == positions['3,1'] != ' '):
        winner = turn
        return True
    if ' ' not in positions.values():
        winner = 'd'
        return True
    return False


def check_move():
    global turn
    global winner
    if move in ['n', 'q']:
        return
    if is_move_valid():
        positions[move] = "X" if turn == 'h' else "O"
        if is_game_finished():
            scores[turn] += 1
            turn = 'd'
        else:
            turn = 'c' if turn == 'h' else 'h'
    else:
        input('Invalid move! Press enter to try again...')


def computer_move():
    global move
    time.sleep(1)
    while True:
        move = f'{random.randint(1, 3)},{random.randint(1, 3)}'
        if is_move_valid():
            break
    print(move)
    time.sleep(1)


while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==============================')
    print('Welcome to Tic-Tac-Toe!')
    print(f'Human: {scores["h"]} | Computer : {scores["c"]}')
    print('==============================')
    print(f' {positions["1,1"]} | {positions["1,2"]} | {positions["1,3"]}')
    print('-----------')
    print(f' {positions["2,1"]} | {positions["2,2"]} | {positions["2,3"]}')
    print('-----------')
    print(f' {positions["3,1"]} | {positions["3,2"]} | {positions["3,3"]}')

    if turn == '':
        turn = input('Who goes first? h (human) or c (computer) or q (quit): ')
        if turn == 'q':
            break
        elif turn not in ['h', 'c']:
            turn = ''
            input('Invalid option! Press enter to continue...')

    if turn == 'd':
        if winner in ['h', 'c']:
            print(f'{"Human" if winner == "h" else "Computer"} wins!!!!!!!!!!!!!')
        elif winner == 'd':
            print('It is a draw!!!!!!!!!!!')
        turn = input(f'n (new game) or q (quit): ')
        if turn not in ['n', 'q']:
            turn = 'd'
            input('Invalid option! Press enter to continue...')

    if turn in ['h', 'c']:
        if turn == 'h':
            move = input('Human, what is the move? row,column or n (new game) or q (quit): ')
            move = move.replace(' ', '')
        elif turn == 'c':
            print('Computer, what is the move? row,column or n (new game) or q (quit): ', end='')
            computer_move()
        check_move()

    if turn == 'n' or move == 'n':
        restart_game()

    if turn == 'q' or move == 'q':
        break
