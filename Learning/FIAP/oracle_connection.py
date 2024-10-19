import os
import cx_Oracle
import pandas as pd

conn = None
cursor = None
margin = ' ' * 4

def reset_id():
    cursor.execute('alter table my_pets modify id number generated always as identity (start with 1)')

try:
    lib_dir = os.environ.get("LD_LIBRARY_PATH")
    cx_Oracle.init_oracle_client(lib_dir=lib_dir)
    conn = cx_Oracle.connect('rm559693', '060180', cx_Oracle.makedsn('oracle.fiap.com.br', 1521, 'orcl'))
    cursor = conn.cursor()
    try:
        cursor.execute('create table my_pets ('
                       'id number generated always as identity primary key,'
                       'pet_type varchar2(20),'
                       'name varchar2(20),'
                       'age number'
                       ')')
    except:
        pass
except Exception as error:
    connected = False
    print(error)
else:
    connected = True

while connected:
    os.system('cls' if os.name == 'nt' else 'clear')
    print('==============================')
    print('Welcome to CRUD Oracle!')
    print('==============================')
    print('1. List')
    print('2. Insert')
    print('3. Update')
    print('4. Delete')
    print('5. Delete all')
    print('6. Exit')
    print('==============================')
    option = int(input('Choose an option: '))
    match option:
        case 1:
            data = cursor.execute('select * from my_pets').fetchall()
            if len(data) > 0:
                print(pd.DataFrame(data=data, columns=['ID', 'Pet Type', 'Name', 'Age']).to_string(index=False))
            else:
                print('No data!')
        case 2:
            try:
                print('Insert')
                pet_type = input(f'{margin}Type: ')
                name = input(f'{margin}Name: ')
                age = int(input(f'{margin}Age: '))
                if pet_type == '' or name == '' or age == '':
                    print('All fields are required!')
                    raise Exception
                else:
                    cursor.execute(f"insert into my_pets (pet_type, name, age) values ('{pet_type}', '{name}', {age})")
                    conn.commit()
            except Exception as error:
                print(error)
            else:
                print('Inserted!')
        case 3:
            try:
                print('Update')
                _id = int(input(f'{margin}ID: '))
                if not cursor.execute(f"select * from my_pets where id = {_id}").fetchone():
                    print('ID not found!')
                    raise Exception
                pet_type = input(f'{margin}Type: ')
                name = input(f'{margin}Name: ')
                age = int(input(f'{margin}Age: '))
                if _id == '' or pet_type == '' or name == '' or age == '':
                    print('All fields are required!')
                    raise Exception
                else:
                    cursor.execute(f"update my_pets set pet_type = '{pet_type}', name = '{name}', age = {age} where id = {_id}")
                    conn.commit()
            except Exception as error:
                print(error)
            else:
                print('Updated!')
        case 4:
            try:
                print('Delete')
                _id = int(input(f'{margin}ID: '))
                if not cursor.execute(f"select * from my_pets where id = {_id}").fetchone():
                    print('ID not found!')
                    raise Exception
                else:
                    cursor.execute(f"delete from my_pets where id = {_id}")
                    count = cursor.execute('select count(*) from my_pets').fetchone()[0]
                    if count == 0:
                        reset_id()
                    conn.commit()
            except Exception as error:
                print(error)
            else:
                print('Deleted!')
        case 5:
            try:
                print('Delete all')
                confirm = input(f'{margin}Are you sure? (y/n): ')
                if confirm.lower() != 'y':
                    raise Exception
                cursor.execute('delete from my_pets where id > 0')
                reset_id()
                conn.commit()
            except Exception as error:
                print(error)
            else:
                print('Deleted!')
        case 6:
            print('Bye!')
            if conn:
                conn.close()
            break
