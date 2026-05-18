# Bank Services

from database import *
import datetime


class Bank:

    def __init__(self, username, account_number):
        self.__username = username
        self.__account_number = account_number

        # Safe table name
        self.__table_name = f"`{username.lower().replace(' ', '_')}_transaction`"

    # Create Transaction Table
    def create_transaction_table(self):

        db_query(
            f"CREATE TABLE IF NOT EXISTS {self.__table_name} ("
            f"timedate DATETIME,"
            f"account_number BIGINT,"
            f"remarks VARCHAR(100),"
            f"amount INTEGER"
            f")"
        )

    # Balance Enquiry
    def balanceequiry(self):

        temp = db_query(
            f"SELECT balance FROM customers "
            f"WHERE username = '{self.__username}';"
        )

        print(f"{self.__username} Balance is {temp[0][0]}")

    # Deposit Money
    def deposit(self, amount):

        temp = db_query(
            f"SELECT balance FROM customers "
            f"WHERE username = '{self.__username}';"
        )

        new_balance = amount + temp[0][0]

        db_query(
            f"UPDATE customers "
            f"SET balance = '{new_balance}' "
            f"WHERE username = '{self.__username}';"
        )

        self.balanceequiry()

        db_query(
            f"INSERT INTO {self.__table_name} VALUES ("
            f"'{datetime.datetime.now()}',"
            f"'{self.__account_number}',"
            f"'Amount Deposited',"
            f"'{amount}'"
            f")"
        )

        print(
            f"{self.__username} Amount Successfully Deposited "
            f"into Your Account {self.__account_number}"
        )

    # Withdraw Money
    def withdraw(self, amount):

        temp = db_query(
            f"SELECT balance FROM customers "
            f"WHERE username = '{self.__username}';"
        )

        current_balance = temp[0][0]

        if amount > current_balance:
            print("Insufficient Balance Please Deposit Money")

        else:

            new_balance = current_balance - amount

            db_query(
                f"UPDATE customers "
                f"SET balance = '{new_balance}' "
                f"WHERE username = '{self.__username}';"
            )

            self.balanceequiry()

            db_query(
                f"INSERT INTO {self.__table_name} VALUES ("
                f"'{datetime.datetime.now()}',"
                f"'{self.__account_number}',"
                f"'Amount Withdrawn',"
                f"'{amount}'"
                f")"
            )

            print(
                f"{self.__username} Amount Successfully Withdrawn "
                f"from Your Account {self.__account_number}"
            )

    # Fund Transfer
    def fundtransfer(self, receive, amount):

        sender_data = db_query(
            f"SELECT balance FROM customers "
            f"WHERE username = '{self.__username}';"
        )

        sender_balance = sender_data[0][0]

        if amount > sender_balance:

            print("Insufficient Balance Please Deposit Money")

        else:

            receiver_data = db_query(
                f"SELECT balance FROM customers "
                f"WHERE account_number = '{receive}';"
            )

            if receiver_data == []:

                print("Account Number Does Not Exist")

            else:

                receiver_balance = receiver_data[0][0]

                sender_new_balance = sender_balance - amount
                receiver_new_balance = receiver_balance + amount

                # Update sender balance
                db_query(
                    f"UPDATE customers "
                    f"SET balance = '{sender_new_balance}' "
                    f"WHERE username = '{self.__username}';"
                )

                # Update receiver balance
                db_query(
                    f"UPDATE customers "
                    f"SET balance = '{receiver_new_balance}' "
                    f"WHERE account_number = '{receive}';"
                )

                # Get receiver username
                receiver_username = db_query(
                    f"SELECT username FROM customers "
                    f"WHERE account_number = '{receive}';"
                )

                receiver_name = receiver_username[0][0]

                # Receiver transaction table
                receiver_table = (
                    f"`{receiver_name.lower().replace(' ', '_')}_transaction`"
                )
                db_query(
                    f"CREATE TABLE IF NOT EXISTS {receiver_table} ("
                    f"timedate DATETIME,"
                    f"account_number BIGINT,"
                    f"remarks VARCHAR(100),"
                    f"amount INTEGER"
                    f")"
                )

                self.balanceequiry()

                # Receiver transaction entry
                db_query(
                    f"INSERT INTO {receiver_table} VALUES ("
                    f"'{datetime.datetime.now()}',"
                    f"'{self.__account_number}',"
                    f"'Fund Transfer From {self.__account_number}',"
                    f"'{amount}'"
                    f")"
                )

                # Sender transaction entry
                db_query(
                    f"INSERT INTO {self.__table_name} VALUES ("
                    f"'{datetime.datetime.now()}',"
                    f"'{self.__account_number}',"
                    f"'Fund Transfer To {receive}',"
                    f"'{amount}'"
                    f")"
                )

                print(
                    f"{self.__username} Amount Successfully "
                    f"Transferred from Your Account "
                    f"{self.__account_number}"
                )

    # Find Account Number
    def find_account(self):

        search = input("Enter Username to Find Account Number: ")

        temp = db_query(
            f"SELECT account_number FROM customers "
            f"WHERE username = '{search}';"
        )

        if temp:

            print(
                f"Account Number of "
                f"{search.capitalize()} is {temp[0][0]}"
            )

        else:

            print(f"No User Found with Username '{search}'")
    
    def delete_account(self):

        confirm = input(
            "Are You Sure You Want to Delete Account? (yes/no): "
        )

        if confirm.lower() == "yes":

            # Delete customer data
            db_query(
                f"DELETE FROM customers "
                f"WHERE username = '{self.__username}';"
            )

            # Delete transaction table
            db_query(
                f"DROP TABLE IF EXISTS {self.__table_name};"
            )

            print("Account Deleted Successfully")

        else:

            print("Account Deletion Cancelled")