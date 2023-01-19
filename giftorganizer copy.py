import hashlib
import os
import time
from os import path
import json

yesinps = ['Yes', 'yes', 'y', 'Y']
noinps = ['No', 'no', 'n', 'N']
COMMAND_LIST = {
    'create': 'Create gifts',
    'modify': 'Modify existing gifts',
    'budget': 'Modify budget',
    'display': 'Display the gifts and budget',
    'exit': "Exit the program (or enter nothing)"
}
MAXIMUM_PEOPLE = 9


class Person:
    def __init__(self, *args) -> None:
        if len(args) == 1:
            person_dict = args[0]

            self.__name = person_dict.get('name')
            self.__gift = person_dict.get('gift')
            self.__price = int(person_dict.get('price'))

        elif len(args) == 3:
            self.__name = args[0]
            self.__gift = args[1]
            self.__price = int(args[2])

    def getDict(self):
        return {'name': self.__name, 'gift': self.__gift, 'price': self.__price}

    def getName(self):
        return self.__name

    def getGift(self):
        return self.__gift

    def getPrice(self):
        return self.__price

    def setName(self, name):
        self.__name = name

    def setGift(self, gift):
        self.__gift = gift

    def setPrice(self, price):
        self.__price = int(price)


def passHasher(password):
    hashed = hashlib.sha256(password.encode('utf-8'))
    hexed = hashed.hexdigest()
    password = hexed

    return password


def passSetup():
    password = input("Set a password: ")
    p = open("password", 'x', encoding="utf-8")
    p.write(passHasher(password))
    p.close()


def passCheck(inp):
    p = open("password", "r", encoding="utf-8")
    if passHasher(inp) == p.read(64):
        p.close()
        print("That is the correct password.")
        time.sleep(1)

        return
    else:
        while True:
            inp = input("Incorrect password. Please try again: ")
            p.seek(0)

            if passHasher(inp) == p.read(64):
                p.close()
                print("That is the correct password.")

                break
            else:

                pass


def checkInt(inp):
    while inp.isdigit() != True:
        inp = input("Please enter an integer or float: ")

    if inp.isdigit():
        if inp.__contains__('.'):
            float(inp)

            return inp
        else:
            int(inp)
            return inp


def updateBudget():
    gifts_data = read_and_parse_json()
    budget = gifts_data.get('budget')

    new_budget_input = input(
        'Enter a budget, or leave blank to keep the original budget of %s: ' % budget)

    if (new_budget_input):
        gifts_data.update({'budget': int(new_budget_input)})
        save_gifts_data(gifts_data)


def setBudget():
    gifts_data = read_and_parse_json()
    budget = gifts_data.get('budget')

    if (not budget):
        new_budget_input = int(input('Enter a budget: '))

        gifts_data.update({'budget': int(new_budget_input)})
        save_gifts_data(gifts_data)


def read_and_parse_json():
    if path.exists('dict.json'):
        with open('dict.json', 'r') as file:
            dict_json = json.load(file)

            return {'gifts': [Person(person_dict) for person_dict in dict_json.get('gifts')], 'budget': dict_json.get('budget')}
    else:
        return {
            'gifts': [],
            'budget': 0
        }


def save_gifts_data(gifts_data):
    gifts_data_json = json.dumps(
        {
            'gifts': [person.getDict() for person in gifts_data.get('gifts')],
            'budget': gifts_data.get('budget')
        },
        indent=3
    )

    with open('dict.json', 'w+') as write:
        write.write(gifts_data_json)

    return


def create_person_from_input():
    person_input = input("Please enter the name of the person: ")
    gift_input = input("Please enter the gift for the person: ")
    price_input = input("Please enter the price of their gift: ")

    return Person(person_input, gift_input, price_input)


def modify_person_from_input(person):
    new_name = input('Enter new name: ')
    if (new_name):
        person.setName(new_name)

    new_gift = input('Enter new gift: ')
    if (new_gift):
        person.setGift(new_gift)

    new_price = input('Enter new price: ')
    if (new_price):
        person.setPrice(new_price)

    return person


def sum_budget(var):
    with open("dict.json", "r+") as check:
        list = json.load(check)
        var = 0
        for entries in list:
            var += (entries['price'])

        check.close()

        return var


def overBudgetCheck(budget):
    total = 0
    sum_budget(total)

    while total > int(budget):
        print("The total price of all gifts exceeds the budget.")
    else:
        print("The total price of all gifts does not exceed the budget.")


def get_people_list_from_json():
    with open("dict.json", "r") as read:
        data = json.load(read)
        people = []
        for x in data:
            people.append(x)
    read.close()

    return people


def create_persons_list():
    gift_data = read_and_parse_json()
    budget = gift_data.get('budget')

    if len(gift_data.get('gifts')) > 0:
        confirmation = input(
            'Gift list already exists, do you want to continue?(y/n) ')
        if confirmation in noinps:
            return

    gifts = []
    for x in range(1, MAXIMUM_PEOPLE):
        print('Budget available: {budget}'.format(budget=budget))
        if budget <= 0:
            print('You are over budget. Consider modifying one of your gifts.')

        new_person = create_person_from_input()
        gifts.append(new_person)
        budget -= new_person.getPrice()
        os.system('cls')

    save_gifts_data({
        **gift_data,
        "gifts": gifts
    })


def update_existing_person():
    gift_data = read_and_parse_json()
    gifts = gift_data.get('gifts')

    if len(gifts) == 0:
        print('No people exist in the file, please create them first.')

        return
    while True:
        person_index = 0
        while person_index not in range(1, (len(gifts) + 1)):
            person_index = int(
                input("Please enter a number 1-%s: " % len(gifts)))

        gifts[person_index -
              1] = modify_person_from_input(gifts[person_index - 1])

        continue_input = input(
            'Do you want to continue to modify another person?(y/n)')
        if continue_input in noinps:
            break

        os.system('cls')

    save_gifts_data({
        **gift_data,
        'gifts': gifts
    })


def display():
    gift_data = read_and_parse_json()
    gifts = gift_data.get('gifts')
    budget = gift_data.get('budget')

    for i, gift in enumerate(gifts):
        print('Gift {gift_index}: \nPerson: {name}\nGift: {gift}\nPrice: {price}\n'.format(
            gift_index=i + 1,
            name=gift.getName(),
            gift=gift.getGift(),
            price=gift.getPrice()
        ))

    print('Budget: {budget}'.format(budget=budget))
    input('Press enter to continue...')


def choose_operation_option():
    while True:
        os.system('cls')

        print('Commands: ')
        for command in COMMAND_LIST:
            print(' - {command}: {command_detail}'.format(
                command=command, command_detail=COMMAND_LIST.get(command)))

        operation_input = input(
            "\nEnter a command from the list above: ")

        match operation_input:
            case 'create':
                setBudget()
                create_persons_list()
            case 'modify':
                update_existing_person()
            case 'budget':
                updateBudget()
            case 'display':
                display()
            case 'exit':
                break
            case default:
                break


def main():
    print("WARNING: This program requires Python 3.10 or newer\n")
    if path.exists('password'):
        print("Password has already been set.")
    else:
        passSetup()

    inp = input("Enter the password to begin: ")
    passCheck(inp)

    print("Welcome to sis's Gift Organizer!")

    choose_operation_option()


main()
