import os

all_cars = {
    "0": {"name": "Sedan", "price": 100},
    "1": {"name": "SUV", "price": 200},
    "2": {"name": "Truck", "price": 300},
    "3": {"name": "Van", "price": 400}
}
rented_cars = {"3": {"name": "Van", "price": 400}}
exit_option = '9'

def available_cars():
    return {i: c for i, c in all_cars.items() if i not in rented_cars}

def wait():
    input("Press enter to continue...")

while True:
    os.system('clear')
    print("Car Rental System")
    print("[1] Rent a Car")
    print("[2] Return a Car")
    print(f"[{exit_option}] Exit")
    operation_option = input('Choose an option: ')
    if operation_option == "1":
        while True:
            os.system('clear')
            print("Choose a car to rent")
            for car_id, car in available_cars().items():
                print(f"[{car_id}] {car['name']} ${car['price']}")
            print(f"[{exit_option}] Cancel")
            rent_option = input('Choose an option: ')
            if rent_option in available_cars():
                rented_cars[rent_option] = available_cars()[rent_option]
                print(f"Rented {all_cars[rent_option]['name']} for ${all_cars[rent_option]['price']}. Enjoy!")
                wait()
                break
            elif rent_option == exit_option:
                break
            else:
                print("Invalid option")
                wait()
    elif operation_option == "2":
        while True:
            os.system('clear')
            print("Choose a car to return")
            for car_id, car in rented_cars.items():
                print(f"[{car_id}] {car['name']} ${car['price']}")
            print(f"[{exit_option}] Cancel")
            return_option = input('Choose an option: ')
            if return_option in rented_cars:
                rented_cars.pop(return_option)
                print(f"Returned {all_cars[return_option]['name']} for ${all_cars[return_option]['price']}. Thank you!")
                wait()
                break
            elif return_option == exit_option:
                break
            else:
                print("Invalid option")
                wait()
    elif operation_option == exit_option:
        break
    else:
        print("Invalid option")
        wait()
