import sqlite3
from initialize_db import initialize_database

DB_NAME = "example.db"


# CREATE ACCOUNT
def create_account():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== CREATE ACCOUNT ===")
    name = input("Enter account holder's name: ")
    balance = float(input("Enter initial deposit amount: "))

    cursor.execute("INSERT INTO account (name, balance) VALUES (?, ?)", (name, balance))

    # Log transaction
    cursor.execute('''
        INSERT INTO transactions (account_name, type, amount)
        VALUES (?, 'create_account', ?)
    ''', (name, balance))

    connection.commit()
    connection.close()

    print(success_message(name, balance))

def success_message(name, balance):
  return f"Account created successfully for {name} with balance {balance}."


def transfer_message(sender, amount):
    return f"Transfer successful! {amount} transferred from {sender}."


# DEPOSIT

def deposit():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== DEPOSIT MONEY ===")
    name = input("Enter account holder's name: ")
    amount = float(input("Enter amount to deposit: "))

    cursor.execute("SELECT balance FROM account WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        connection.close()
        return

    new_balance = result[0] + amount

    cursor.execute("UPDATE account SET balance = ? WHERE name = ?", (new_balance, name))

    # Log transaction
    cursor.execute('''
        INSERT INTO transactions (account_name, type, amount)
        VALUES (?, 'deposit', ?)
    ''', (name, amount))

    connection.commit()
    connection.close()

    print(f"Deposit successful! New balance for {name}: {new_balance}")



# WITHDRAW

def withdraw():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== WITHDRAW MONEY ===")
    name = input("Enter account holder's name: ")
    amount = float(input("Enter amount to withdraw: "))

    cursor.execute("SELECT balance FROM account WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        connection.close()
        return

    current_balance = result[0]

    if current_balance < amount:
        print("Insufficient funds. Withdrawal cancelled.")
        connection.close()
        return

    new_balance = current_balance - amount

    cursor.execute("UPDATE account SET balance = ? WHERE name = ?", (new_balance, name))

    # Log transaction
    cursor.execute('''
        INSERT INTO transactions (account_name, type, amount)
        VALUES (?, 'withdraw', ?)
    ''', (name, amount))

    connection.commit()
    connection.close()

    print(f"Withdrawal successful! New balance for {name}: {new_balance}")



# TRANSFER

def transfer():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== TRANSFER MONEY ===")
    sender = input("Enter sender's name: ")
    receiver = input("Enter receiver's name: ")
    amount = float(input("Enter amount to transfer: "))

    cursor.execute("SELECT balance FROM account WHERE name = ?", (sender,))
    sender_result = cursor.fetchone()

    if sender_result is None:
        print("Sender account not found.")
        connection.close()
        return

    cursor.execute("SELECT balance FROM account WHERE name = ?", (receiver,))
    receiver_result = cursor.fetchone()

    if receiver_result is None:
        print("Receiver account not found.")
        connection.close()
        return

    sender_balance = sender_result[0]

    if sender_balance < amount:
        print("Insufficient funds. Transfer cancelled.")
        connection.close()
        return

    new_sender_balance = sender_balance - amount
    new_receiver_balance = receiver_result[0] + amount

    cursor.execute("UPDATE account SET balance = ? WHERE name = ?", (new_sender_balance, sender))
    cursor.execute("UPDATE account SET balance = ? WHERE name = ?", (new_receiver_balance, receiver))

    # Log transactions
    cursor.execute('''
        INSERT INTO transactions (account_name, type, amount)
        VALUES (?, 'transfer_out', ?)
    ''', (sender, amount))

    cursor.execute('''
        INSERT INTO transactions (account_name, type, amount)
        VALUES (?, 'transfer_in', ?)
    ''', (receiver, amount))

    connection.commit()
    connection.close()

    print(transfer_message(sender, amount))



# DELETE ACCOUNT

def delete_account():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== DELETE ACCOUNT ===")
    name = input("Enter the name of the account to delete: ")

    cursor.execute("SELECT * FROM account WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
        connection.close()
        return

    confirm = input(f"Are you sure you want to delete '{name}'? (yes/no): ").lower()

    if confirm != "yes":
        print("Deletion cancelled.")
        connection.close()
        return

    cursor.execute("DELETE FROM account WHERE name = ?", (name,))
    connection.commit()
    connection.close()

    print(f"Account '{name}' deleted successfully.")



# CHECK BALANCE

def check_balance():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== CHECK BALANCE ===")
    name = input("Enter account holder's name: ")

    cursor.execute("SELECT balance FROM account WHERE name = ?", (name,))
    result = cursor.fetchone()

    if result is None:
        print("Account not found.")
    else:
        print(f"{name}'s balance: {result[0]}")

    connection.close()


# VIEW TRANSACTIONS
def view_transactions():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    print("=== TRANSACTION HISTORY ===")
    name = input("Enter account holder's name: ")

    cursor.execute('''
        SELECT type, amount, timestamp
        FROM transactions
        WHERE account_name = ?
        ORDER BY timestamp DESC
    ''', (name,))

    results = cursor.fetchall()

    if not results:
        print("No transactions found.")
    else:
        for t in results:
            print(f"{t[2]} | {t[0]} | Amount: {t[1]}")

    connection.close()



# VIEW ACCOUNTS

def view_accounts():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("SELECT id, name, balance FROM account")
    accounts = cursor.fetchall()

    print("=== ACCOUNTS ===")
    for acc in accounts:
        print(f"ID: {acc[0]} | Name: {acc[1]} | Balance: {acc[2]}")

    connection.close()



# MENU
def welcome_menu():
    while True:
        print("\n--- Welcome Menu ---")
        print("1. Create Account")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. View Accounts")
        print("6. Exit")
        print("7. Delete Account")
        print("8. Check Balance")
        print("9. View Transactions")

        choice = input("\nEnter your choice: ")

        if choice == "1":
            create_account()
        elif choice == "2":
            deposit()
        elif choice == "3":
            withdraw()
        elif choice == "4":
            transfer()
        elif choice == "5":
            view_accounts()
        elif choice == "6":
            print("Goodbye!")
            break
        elif choice == "7":
            delete_account()
        elif choice == "8":
            check_balance()
        elif choice == "9":
            view_transactions()
        else:
            print("Invalid choice.")


# RUN PROGRAM

if __name__ == "__main__":
    initialize_database()
    welcome_menu()
