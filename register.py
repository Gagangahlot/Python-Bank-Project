#User Registration Signin Signup
from customer import *
from bank import Bank
import random

def SignUp():
    username = input("Create Username: ")
    temp = db_query(f"SELECT username FROM customers where username = '{username}';")
    if temp:
        print("Username Already Exists")
        SignUp()
    else:
        print("Username is Available Please Proceed")
        password = input("Enter Your Password: ")
        name = input("Enter Your Name: ")
        age = input("Enter Your Age: ")
        city = input("Enter Your City: ")
        while True:
            account_number = int(random.randint(10000000, 99999999))
            temp = db_query(f"SELECT account_number FROM customers WHERE account_number = '{account_number}';")
            if temp:
                continue
            else:
                print("Your Account Number",account_number)
                break
    cobj = Customer(username, password, name, age, city, account_number)
    cobj.createuser()
    bobj = Bank(username, account_number)
    bobj.create_transaction_table()

def SignIn():
    attempts = 0
    max_attempts = 2

    while attempts < max_attempts:
        username = input("Enter Username: ")
        temp = db_query(f"SELECT username FROM customers WHERE username = '{username}';")

        if temp:
            while True:
                password = input(f"Welcome {username.capitalize()} Enter Password: ")
                temp = db_query(f"SELECT password FROM customers WHERE username = '{username}';")
                if temp[0][0] == password:
                    print("Signed In Successfully")
                    return username
                else:
                    print("Wrong Password, Try Again")
                    continue
        else:
            attempts += 1
            remaining = max_attempts - attempts
            if remaining > 0:
                print(f"Username not found. {remaining} attempt(s) remaining.")
            else:
                print("Too many failed attempts. Redirecting to main menu...\n")

    return None  # Signal that sign-in failed
