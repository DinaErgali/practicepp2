import csv
import psycopg2
from connect import get_connection


# CREATE TABLE
def create_table():
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS contacts (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        phone VARCHAR(20) UNIQUE
    );
    """)

    conn.commit()
    cur.close()
    conn.close()


# INSERT FROM CSV
def insert_from_csv():
    conn = get_connection()
    cur = conn.cursor()
    
    with open("contacts.csv", "r") as f:
        for row in csv.DictReader(f):
            try:
                cur.execute(
                    "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
                    (row["name"], row["phone"])
                )
            except psycopg2.IntegrityError:
                conn.rollback()  # 重复就跳过
    
    conn.commit()
    cur.close()
    conn.close()
    print("CSV data inserted")


# INSERT FROM CONSOLE
def insert_manual():
    name = input("Enter name: ")
    phone = input("Enter phone: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "INSERT INTO contacts (name, phone) VALUES (%s, %s)",
        (name, phone)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Contact added")


# QUERY WITH FILTERS
def query_contacts():
    print("\n1. Show all")
    print("2. Search by name")
    print("3. Search by phone prefix")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        cur.execute("SELECT * FROM contacts")

    elif choice == "2":
        name = input("Enter name: ")
        cur.execute(
            "SELECT * FROM contacts WHERE name ILIKE %s",
            (f"%{name}%",)
        )

    elif choice == "3":
        prefix = input("Enter phone prefix: ")
        cur.execute(
            "SELECT * FROM contacts WHERE phone LIKE %s",
            (f"{prefix}%",)
        )

    rows = cur.fetchall()
    for row in rows:
        print(row)

    cur.close()
    conn.close()


# UPDATE CONTACT
def update_contact():
    name = input("Enter current name: ")

    print("1. Update name")
    print("2. Update phone")

    choice = input("Choose: ")

    conn = get_connection()
    cur = conn.cursor()

    if choice == "1":
        new_name = input("Enter new name: ")
        cur.execute(
            "UPDATE contacts SET name = %s WHERE name = %s",
            (new_name, name)
        )

    elif choice == "2":
        new_phone = input("Enter new phone: ")
        cur.execute(
            "UPDATE contacts SET phone = %s WHERE name = %s",
            (new_phone, name)
        )

    conn.commit()
    cur.close()
    conn.close()
    print("Updated successfully")


# DELETE CONTACT
def delete_contact():
    value = input("Enter name OR phone to delete: ")

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM contacts WHERE name = %s OR phone = %s",
        (value, value)
    )

    conn.commit()
    cur.close()
    conn.close()
    print("Deleted successfully")


# MAIN MENU
def main():
    create_table()

    while True:
        print("\n--- PHONEBOOK MENU ---")
        print("1. Insert from CSV")
        print("2. Insert manually")
        print("3. Query contacts")
        print("4. Update contact")
        print("5. Delete contact")
        print("6. Exit")

        choice = input("Choose: ")

        if choice == "1":
            insert_from_csv()
        elif choice == "2":
            insert_manual()
        elif choice == "3":
            query_contacts()
        elif choice == "4":
            update_contact()
        elif choice == "5":
            delete_contact()
        elif choice == "6":
            break


if __name__ == "__main__":
    main()