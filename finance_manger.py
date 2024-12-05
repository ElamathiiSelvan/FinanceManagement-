import sqlite3

# Database Connection
def get_db_connection():
    conn = sqlite3.connect("finance_manager.db")
    return conn

# Database Setup
def setup_database():
    conn = get_db_connection()
    conn.executescript("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password TEXT NOT NULL
    );

    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        category TEXT NOT NULL,
        amount REAL NOT NULL,
        type TEXT NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id)
    );
    """)
    conn.close()
    print("Database setup complete!")

# User Registration
def register_user(username, password):
    conn = get_db_connection()
    try:
        conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?)", (username, password)
        )
        conn.commit()
        print("Registration successful!")
    except sqlite3.IntegrityError:
        print("Error: Username already exists.")
    finally:
        conn.close()

# User Login
def login_user(username, password):
    conn = get_db_connection()
    user = conn.execute(
        "SELECT id FROM users WHERE username = ? AND password = ?", (username, password)
    ).fetchone()
    conn.close()
    if user:
        return user[0]  # Return user ID
    return None

# Add Transaction
def add_transaction(user_id, category, amount, type_):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO transactions (user_id, category, amount, type) VALUES (?, ?, ?, ?)",
        (user_id, category, amount, type_),
    )
    conn.commit()
    conn.close()
    print("Transaction added successfully!")

# View Transactions
def view_transactions(user_id):
    conn = get_db_connection()
    transactions = conn.execute(
        "SELECT category, amount, type FROM transactions WHERE user_id = ?", (user_id,)
    ).fetchall()
    conn.close()
    return transactions

# Generate Financial Report
def generate_report(user_id):
    conn = get_db_connection()
    transactions = conn.execute(
        "SELECT type, SUM(amount) FROM transactions WHERE user_id = ? GROUP BY type",
        (user_id,),
    ).fetchall()
    conn.close()

    total_income = 0
    total_expense = 0
    for t_type, total in transactions:
        if t_type == "income":
            total_income += total
        elif t_type == "expense":
            total_expense += total

    savings = total_income - total_expense
    print("\n--- Financial Report ---")
    print(f"Total Income: {total_income}")
    print(f"Total Expense: {total_expense}")
    print(f"Savings: {savings}\n")

# Main Application
def main():
    setup_database()

    print("Welcome to the Personal Finance Manager!")
    while True:
        print("\n1. Register\n2. Login\n3. Exit")
        choice = input("Enter your choice: ")
        
        if choice == "1":
            username = input("Enter username: ")
            password = input("Enter password: ")
            register_user(username, password)
        
        elif choice == "2":
            username = input("Enter username: ")
            password = input("Enter password: ")
            user_id = login_user(username, password)
            if user_id:
                print("Login successful!")
                while True:
                    print("\n1. Add Transaction\n2. View Transactions\n3. Generate Report\n4. Logout")
                    user_choice = input("Enter your choice: ")
                    
                    if user_choice == "1":
                        category = input("Enter category: ")
                        amount = float(input("Enter amount: "))
                        type_ = input("Enter type (income/expense): ").lower()
                        add_transaction(user_id, category, amount, type_)
                    
                    elif user_choice == "2":
                        transactions = view_transactions(user_id)
                        print("\n--- Your Transactions ---")
                        for t in transactions:
                            print(f"Category: {t[0]}, Amount: {t[1]}, Type: {t[2]}")
                    
                    elif user_choice == "3":
                        generate_report(user_id)
                    
                    elif user_choice == "4":
                        print("Logged out successfully.")
                        break
                    
                    else:
                        print("Invalid choice. Try again.")
            else:
                print("Login failed. Invalid credentials.")
        
        elif choice == "3":
            print("Exiting the application. Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "_main_":
    main()