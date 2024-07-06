import os
import random

options = {
    '1': 'Rock',
    '2': 'Paper',
    '3': 'Scissors'
}
scores = {
    'user': 0,
    'computer': 0
}

while True:
    os.system('clear')
    computer_option = str(random.randint(1, 3))
    print('======================================================')
    print(f'Rock, Paper, Scissors Game :: User({str(scores["user"])}) vs Computer({str(scores["computer"])})')
    print('------------------------------------------------------')
    for i in options:
        print(f'{i}. {options[i]}')
    print('4. Quit')
    user_option = input('Choose an option: ')

    if user_option == '4':
        break
    elif user_option not in ['1', '2', '3']:
        print('Invalid option!')
    elif user_option == computer_option:
        scores['computer'] += 1
        scores['user'] += 1
        print(f'Draw!\nUser({str(scores["user"])}) vs Computer({str(scores["computer"])})')
    elif (user_option, computer_option) in (('1', '3'), ('2', '1'), ('3', '2')):
        scores['user'] += 1
        print(f'User wins! {options[user_option]} beats {options[computer_option]}\nUser({str(scores["user"])}) vs Computer({str(scores["computer"])})')
    elif (user_option, computer_option) in (('3', '1'), ('1', '2'), ('2', '3')):
        scores['computer'] += 1
        print(f'Computer wins! {options[computer_option]} beats {options[user_option]}\nUser({str(scores["user"])}) vs Computer({str(scores["computer"])})')
    input('Press enter to continue...')
