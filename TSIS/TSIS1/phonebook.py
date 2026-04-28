import json
import csv
from connect import get_connection

# ------------------- ADD CONTACT -------------------
def add_contact(conn):
    name = input("Name: ")
    email = input("Email: ")
    birthday = input("Birthday (YYYY-MM-DD): ")
    group = input("Group: ")

    cur = conn.cursor()

    # group
    cur.execute("SELECT id FROM groups WHERE name=%s", (group,))
    g = cur.fetchone()

    if not g:
        cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group,))
        group_id = cur.fetchone()[0]
    else:
        group_id = g[0]

    cur.execute("""
        INSERT INTO contacts(name, email, birthday, group_id)
        VALUES (%s, %s, %s, %s)
    """, (name, email, birthday, group_id))

    conn.commit()
    print("Added!")

# ------------------- ADD PHONE -------------------
def add_phone(conn):
    name = input("Contact name: ")
    phone = input("Phone: ")
    ptype = input("Type (home/work/mobile): ")

    cur = conn.cursor()
    cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
    conn.commit()

# ------------------- SEARCH -------------------
def search(conn):
    q = input("Search: ")
    cur = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (q,))
    rows = cur.fetchall()

    for r in rows:
        print(r)

# ------------------- FILTER GROUP -------------------
def filter_group(conn):
    g = input("Group: ")
    cur = conn.cursor()

    cur.execute("""
        SELECT c.name, c.email
        FROM contacts c
        JOIN groups g ON c.group_id = g.id
        WHERE g.name=%s
    """, (g,))

    for r in cur.fetchall():
        print(r)

# ------------------- EXPORT JSON -------------------
def export_json(conn):
    cur = conn.cursor()
    cur.execute("""
    SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    """)

    data = cur.fetchall()

    with open("contacts.json", "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, default=str)

    print("Exported!")

# ------------------- IMPORT JSON -------------------
def import_json(conn):
    cur = conn.cursor()

    with open("contacts.json", encoding="utf-8") as f:
        data = json.load(f)

    for row in data:
        name, email, birthday, group_name, phone, ptype = row

        # check duplicate
        cur.execute("SELECT id FROM contacts WHERE name=%s", (name,))
        exists = cur.fetchone()

        if exists:
            choice = input(f"{name} exists. skip/overwrite: ")
            if choice == "skip":
                continue
            else:
                cur.execute("DELETE FROM contacts WHERE name=%s", (name,))

        # group
        cur.execute("SELECT id FROM groups WHERE name=%s", (group_name,))
        g = cur.fetchone()

        if not g:
            cur.execute("INSERT INTO groups(name) VALUES (%s) RETURNING id", (group_name,))
            group_id = cur.fetchone()[0]
        else:
            group_id = g[0]

        # insert contact
        cur.execute("""
            INSERT INTO contacts(name, email, birthday, group_id)
            VALUES (%s, %s, %s, %s)
            RETURNING id
        """, (name, email, birthday, group_id))

        contact_id = cur.fetchone()[0]

        # insert phone
        if phone:
            cur.execute("""
                INSERT INTO phones(contact_id, phone, type)
                VALUES (%s, %s, %s)
            """, (contact_id, phone, ptype))

    conn.commit()
    print("JSON Imported!")

# ------------------- IMPORT CSV -------------------
def import_csv(conn):
    cur = conn.cursor()

    try:
        with open("contacts.csv", newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                # group
                cur.execute("SELECT id FROM groups WHERE name=%s", (row['group'],))
                g = cur.fetchone()

                if not g:
                    cur.execute(
                        "INSERT INTO groups(name) VALUES (%s) RETURNING id",
                        (row['group'],)
                    )
                    group_id = cur.fetchone()[0]
                else:
                    group_id = g[0]

                # contact
                cur.execute("""
                    INSERT INTO contacts(name, email, birthday, group_id)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                """, (row['name'], row['email'], row['birthday'], group_id))

                contact_id = cur.fetchone()[0]

                # phone
                cur.execute("""
                    INSERT INTO phones(contact_id, phone, type)
                    VALUES (%s, %s, %s)
                """, (contact_id, row['phone'], row['type']))

        conn.commit()
        print("CSV Imported!")

    except FileNotFoundError:
        print("contacts.csv not found!")


# ------------------- SHOW ALL CONTACTS -------------------
def show_all(conn):
    cur = conn.cursor()

    cur.execute("""
    SELECT c.name, c.email, c.birthday, g.name, p.phone, p.type
    FROM contacts c
    LEFT JOIN groups g ON c.group_id = g.id
    LEFT JOIN phones p ON c.id = p.contact_id
    ORDER BY c.name
    """)

    rows = cur.fetchall()

    if not rows:
        print("No contacts found.")
        return

    for r in rows:
        print(r)

# ------------------- MENU -------------------
def menu():
    conn = get_connection()

    while True:
        print("""
1 Add Contact
2 Add Phone
3 Search
4 Filter Group
5 Export JSON
6 Import JSON
7 Exit
8 Import CSV
9 Show All Contacts
""")

        choice = input(">> ")

        if choice == "1":
            add_contact(conn)

        elif choice == "2":
            add_phone(conn)

        elif choice == "3":
            search(conn)

        elif choice == "4":
            filter_group(conn)

        elif choice == "5":
            export_json(conn)

        elif choice == "6":
            import_json(conn)

        elif choice == "7":
            print("Bye!")
            break

        elif choice == "8":
            import_csv(conn)

        elif choice == "9":
            show_all(conn)

        else:
            print("Invalid choice!")

    conn.close()


if __name__ == "__main__":
    menu()