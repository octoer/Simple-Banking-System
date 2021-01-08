# Write your code here
import random
import sqlite3

account = {}


def create_account():
    return '400000' + str(random.randint(0, 999999999)).zfill(9) + '?'


def check_digit(wait_check: str):
    check_luhn = list(wait_check)[-1]
    sum_num = list(wait_check)[0:15]
    # sum_num = list(num)
    for i in range(0, 15):
        sum_num[i] = int(sum_num[i])
        if i % 2 == 0:
            if sum_num[i] <= 4:
                sum_num[i] = int(sum_num[i] * 2)
            else:
                sum_num[i] = int(sum_num[i] * 2) - 9
    luhn = str(10 - (sum(sum_num) % 10)) if sum(sum_num) % 10 != 0 else '0'
    if check_luhn == luhn:
        return True
    elif check_luhn == '?':
        check_num = wait_check.strip('?') + luhn
        print(f"Your card has been created\nYour card number:\n{check_num}")
        return check_num
    else:
        return False


def create_pin():
    pin = str(random.randint(0, 9999)).zfill(4)
    print(f"Your card PIN:\n{pin}")
    return pin


def check_balance(command):
    with conn:
        number = (command,)
        cur.execute('SELECT balance FROM card WHERE number = ?', number)
        return cur.fetchone()[0]


def increase_balance(command, increase):
    with conn:
        cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (increase, command))


def do_transfer(receiving_number):
    if card_num == receiving_number:
        print("You can't transfer money to the same account!\n")
    elif check_card(receiving_number):
        if check_digit(payee_card_number):
            money = int(input("Enter how much money you want to transfer: \n"))
            if check_balance(card_num) >= money:
                with conn:
                    cur.execute('UPDATE card SET balance = balance + ? WHERE number = ?', (money, receiving_number))
                    cur.execute('UPDATE card SET balance = balance - ? WHERE number = ?', (money, card_num))
                    print("Success!")
            else:
                print("Not enough money!\n")
        else:
            print("Probably you made a mistake in the card number. Please try again!\n")
    else:
        print("Such a card does not exist.\n")


def close_account(command):
    with conn:
        number = (command,)
        cur.execute('DELETE FROM card WHERE number = ?', number)
        print("The account has been closed!\n")


def check_card(receiving_number):
    with conn:
        num = (receiving_number,)
        cur.execute('SELECT number FROM card WHERE number=?', num)
        return cur.fetchone()


with sqlite3.connect('card.s3db') as conn:
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS card
                 (id INTEGER, number TEXT, pin TEXT, balance INTEGER DEFAULT 0)''')
    while True:
        greet = "1. Create an account\n2. Log into account\n0. Exit\n"
        start = int(input(greet))
        if start == 0:
            print('Bye!')
            exit()
        elif start == 1:
            card_num = check_digit(create_account())
            password = create_pin()
            account[card_num] = password
            with conn:
                cur.execute("INSERT INTO card(number,pin) VALUES (?, ?)", (card_num, password))
            continue
        else:
            card_num = input("Enter your card number:\n")
            password = input("Enter your PIN:\n")
            if account.get(card_num) == password:
                print("You have successfully logged in!\n")
                while True:
                    third = int(input("1. Balance\n2. Add income\n3. Do transfer\n"
                                      "4. Close account\n5. Log out\n0. Exit\n"))
                    if third == 0:
                        print('Bye!')
                        exit()
                    elif third == 1:
                        print(f"Balance: {check_balance(card_num)}")
                        continue
                    elif third == 2:
                        income = int(input("Enter income: \n"))
                        with conn:
                            cur.execute('UPDATE card SET balance=balance+? WHERE number = ?', (income, card_num))
                        continue
                    elif third == 3:
                        payee_card_number = input("Enter card number: \n")
                        if check_digit(payee_card_number):
                            do_transfer(payee_card_number)
                            continue
                        else:
                            print("Probably you made a mistake in the card number. Please try again!")
                    elif third == 4:
                        close_account(card_num)
                        break
                    else:
                        print("You have successfully logged out!")
                        break
            else:
                print("Wrong card number or PIN!")
                continue
