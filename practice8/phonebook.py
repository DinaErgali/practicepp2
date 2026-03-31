from connect import get_connection

conn = get_connection()
cursor = conn.cursor()

# 1. Search by pattern
def search_contacts():
    pattern = input("Enter name or phone pattern: ")
    cursor.execute("SELECT * FROM search_contacts(%s)", (pattern,))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("Nothing found.")

# 2. Upsert - insert or update
def upsert_contact():
    name = input("Enter name: ")
    phone = input("Enter phone: ")
    cursor.execute("CALL upsert_contact(%s, %s)", (name, phone))
    conn.commit()
    print("Contact saved.")

# 3. Mass insert
def insert_many():
    contacts = []
    print("Enter contacts (empty name to finish):")
    while True:
        name = input("Name: ")
        if not name:
            break
        phone = input("Phone: ")
        contacts.append([name, phone])
    
    if contacts:
        cursor.execute("CALL insert_many_contacts(%s)", (contacts,))
        conn.commit()
        print("Contacts processed.")

# 4. Pagination
def get_paginated():
    limit = int(input("How many records to show: "))
    offset = int(input("Starting from record (0 = beginning): "))
    cursor.execute("SELECT * FROM get_contacts_paginated(%s, %s)", (limit, offset))
    rows = cursor.fetchall()
    if rows:
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
    else:
        print("No records found.")

# 5. Delete
def delete_contact():
    print("Delete by:")
    print("1 - Name")
    print("2 - Phone")
    choice = input("Choice: ")
    if choice == "1":
        value = input("Enter name: ")
        cursor.execute("CALL delete_contact(%s, %s)", (value, "name"))
    elif choice == "2":
        value = input("Enter phone: ")
        cursor.execute("CALL delete_contact(%s, %s)", (value, "phone"))
    conn.commit()
    print("Contact deleted.")

# Menu
def main():
    while True:
        print("\n=== PhoneBook Practice 8 ===")
        print("1 - Search by pattern")
        print("2 - Add / Update contact")
        print("3 - Mass insert")
        print("4 - Show with pagination")
        print("5 - Delete contact")
        print("0 - Exit")
        choice = input("Choice: ")

        if choice == "1":
            search_contacts()
        elif choice == "2":
            upsert_contact()
        elif choice == "3":
            insert_many()
        elif choice == "4":
            get_paginated()
        elif choice == "5":
            delete_contact()
        elif choice == "0":
            break

    cursor.close()
    conn.close()

main()