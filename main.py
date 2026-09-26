import sqlite3

# Connect to database
conn = sqlite3.connect("bank.db")
cursor = conn.cursor()

# Create accounts table
cursor.execute("""
CREATE TABLE IF NOT EXISTS accounts (
    account_no INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    balance REAL DEFAULT 0
)
""")
conn.commit()


class BankAccount:
    def __init__(self, account_no, name, balance=0):
        self.account_no = account_no
        self.name = name
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            self.update_database()
            print(f"₹{amount} deposited successfully.")
        else:
            print("Invalid amount.")

    def withdraw(self, amount):
        if amount <= 0:
            print("Invalid amount.")
        elif amount > self.balance:
            print("Insufficient balance.")
        else:
            self.balance -= amount
            self.update_database()
            print(f"₹{amount} withdrawn successfully.")

    def check_balance(self):
        print(f"Current Balance: ₹{self.balance}")

    def update_database(self):
        cursor.execute(
            "UPDATE accounts SET balance = ? WHERE account_no = ?",
            (self.balance, self.account_no)
        )
        conn.commit()


def create_account():
    account_no = int(input("Enter Account Number: "))
    name = input("Enter Account Holder Name: ")
    initial_balance = float(input("Enter Initial Balance: "))

    cursor.execute(
        "INSERT INTO accounts VALUES (?, ?, ?)",
        (account_no, name, initial_balance)
    )
    conn.commit()

    print("Account created successfully!")


def login():
    account_no = int(input("Enter Account Number: "))

    cursor.execute(
        "SELECT * FROM accounts WHERE account_no = ?",
        (account_no,)
    )

    account = cursor.fetchone()

    if account:
        bank_account = BankAccount(
            account[0],
            account[1],
            account[2]
        )

        while True:
            print("\n--- Banking Menu ---")
            print("1. Deposit")
            print("2. Withdraw")
            print("3. Check Balance")
            print("4. Logout")

            choice = input("Enter your choice: ")

            if choice == "1":
                amount = float(input("Enter amount: "))
                bank_account.deposit(amount)

            elif choice == "2":
                amount = float(input("Enter amount: "))
                bank_account.withdraw(amount)

            elif choice == "3":
                bank_account.check_balance()

            elif choice == "4":
                print("Logged out successfully.")
                break

            else:
                print("Invalid choice.")

    else:
        print("Account not found.")


# Main program
while True:
    print("\n===== ONLINE BANKING SYSTEM =====")
    print("1. Create Account")
    print("2. Login")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        create_account()

    elif choice == "2":
        login()

    elif choice == "3":
        print("Thank you for using the Banking System!")
        break

    else:
        print("Invalid choice.")

conn.close()