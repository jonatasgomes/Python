import json

part = 2

if part == 1:
    people = {
        'person1': {
            'name': 'Matheus',
            'age': 23,
            'email': 'm@b.com'
        },
        'person2': {
            'name': 'Gabriela',
            'age': 22,
            'email': 'g@b.com'
        },
        'person3': {
            'name': 'Lucas',
            'age': 21,
            'email': 'l@b.com'
        }
    }
    people_json = json.dumps(people, indent=2)
    with open('file_json.json', 'w') as file:
        file.write(people_json)
else:
    with open('file_json.json', 'r') as file:
        people_json = file.read()
        people = json.loads(people_json)

    for k, v in people.items():
        print(k)
        for k2, v2 in v.items():
            print(f'\t{k2}: {v2}')
