import os
import time

positions = {
    '1,1': ' ', '1,2': ' ', '1,3': ' ',
    '2,1': ' ', '2,2': 'X', '2,3': ' ',
    '3,1': ' ', '3,2': ' ', '3,3': ' '
}
scores = {
    'human': 0,
    'computer': 0
}
turn = ''
move = ''

while True:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==============================')
    print('Welcome to Tic-Tac-Toe!')
    print(f'Human: {scores["human"]} | Computer : {scores["computer"]}')
    print('==============================')
    print(f' {positions["1,1"]} | {positions["1,2"]} | {positions["1,3"]}')
    print('-----------')
    print(f' {positions["2,1"]} | {positions["2,2"]} | {positions["2,3"]}')
    print('-----------')
    print(f' {positions["3,1"]} | {positions["3,2"]} | {positions["3,3"]}')

    if turn == '':
        turn = input('Who goes first? h (human) or c (computer): ')
        if turn in ['h', 'c']:
            print('Ok. ' + turn + ' goes first.')
        else:
            turn = ''
            print('Invalid input. Must be h or c.')
            time.sleep(2)
            continue
    if turn == 'h':
        print('Ok, human goes first.')
        move = input('What is your move? (row,column)')
