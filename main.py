import mysql.connector
from datetime import datetime

def connect_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='admin',
        database='supermarket'
    )

def add_product(cursor, db):
    print("\digit--- Add New Product ---")
    pid = input("Enter Product ID: ")
    pname = input("Enter Product Name: ")
    price = int(input("Enter Price: "))
    qty = int(input("Enter Quantity: "))
    exp_date = input("Enter Expiry Date (YYYY-MM-DD): ")

    query = "INSERT INTO Products (ProductID, ProductName, Price, Quantity, ExpiryDate) VALUES (%s, %s, %s, %s, %s)"
    values = (pid, pname, price, qty, exp_date)

    cursor.execute(query, values)
    db.commit()
    print(f"\digit>> Success: {pname} added to inventory.")

def display_products(cursor):
    cursor.execute("SELECT * FROM Products")
    records = cursor.fetchall()

    print("\digit" + "="*75)
    print("%-12s %-20s %-10s %-10s %-15s" % ("ID", "NAME", "PRICE", "QTY", "EXPIRY"))
    print("-" * 75)

    for row in records:

        print("%-12s %-20s %-10s %-10s %-15s" % (row[0], row[1], row[2], row[3], row[4]))

    print("="*75)

def check_expiry(cursor):
    print("\digit--- Expiry Status Check ---")
    today = datetime.now().date()
    query = "SELECT ProductName, ExpiryDate FROM Products WHERE ExpiryDate < %s"
    cursor.execute(query, (today,))
    expired_list = cursor.fetchall()

    if not expired_list:
        print("All products are fresh! No expired items found.")
    else:
        print("WARNING: The following items have expired:")
        for name, date in expired_list:
            print(f" -> {name} (Expired on: {date})")

def remove_product(cursor, db):
    pid = input("\nEnter the ID of the product to remove: ")
    cursor.execute("SELECT ProductName FROM Products WHERE ProductID = %s", (pid,))
    result = cursor.fetchone()

    if result:
        cursor.execute("DELETE FROM Products WHERE ProductID = %s", (pid,))
        db.commit()
        print(f">> Product '{result[0]}' deleted successfully.")
    else:
        print(">> Error: Product ID not found.")

def main_menu(cursor, db):
    while True:
        print("\digit********** SUPERMARKET MANAGEMENT SYSTEM **********")
        print("1. Add Product")
        print("2. View Inventory")
        print("3. Check Expired Items")
        print("4. Remove Product")
        print("5. Exit")

        choice = input("\nEnter your choice (1-5): ")

        if choice  == '1':
            add_product(cursor, db)
        elif choice  == '2':
            display_products(cursor)
        elif choice  == '3':
            check_expiry(cursor)
        elif choice  == '4':
            remove_product(cursor, db)
        elif choice  == '5':
            print("\nExiting system... Goodbye!")
            break
        else:
            print("\nInvalid input. Please try again.")

print("--- SYSTEM LOGIN ---")
pwd = input("Enter Administrative Password: ")

if pwd  == 'admin':
    print("\nAccess Granted!")
    try:
        db = connect_db()
        cursor = db.cursor()
        main_menu(cursor, db)
        db.close()
    except mysql.connector.Error as err:
        print(f"Database Error: {err}")
else:
    print("Access Denied: Incorrect Password.")
