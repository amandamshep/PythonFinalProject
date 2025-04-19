# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/


# read reservation csv here
# are we doing a reservations class?

# Sherin's code starts after here

import sqlite3
from datetime import datetime
import os
os.chdir(r"C:\Users\varun\Box Sync\Business Analytics Degree\Semesters\Spring Semester 2025\IS 6495\Project\Database_02")

DB_NAME = "HotelReservations.sqlite"


def connect_db():
    #Connect to DB
    return sqlite3.connect(DB_NAME)


def get_available_rooms(conn, room_type):
    #Show available rooms not already booked for the dates
    cursor = conn.cursor()
    if room_type.lower() == 'regular':
        cursor.execute("""
            SELECT r.ROOM_ID, r.TYPE, r.COST
            FROM Regular r
            WHERE r.ROOM_ID NOT IN (
                SELECT ROOM_ID_REG FROM Reservation
                WHERE DATE('now') BETWEEN BEGINNING_DATE AND END_DATE
            )
        """)
    elif room_type.lower() == 'penthouse':
        cursor.execute("""
            SELECT p.ROOM_ID, p.TYPE, p.COST
            FROM Penthouse p
            WHERE p.ROOM_ID NOT IN (
                SELECT ROOM_ID_PENT FROM Reservation
                WHERE DATE('now') BETWEEN BEGINNING_DATE AND END_DATE
            )
        """)
    else:
        return []
    return cursor.fetchall()


def create_reservation():
    #Create a new reservation
    conn = connect_db()
    cursor = conn.cursor()
    try:
        name = input("Enter your full name (First and Last): ").strip()
        email = input("Enter your email address: ").strip()
        room_type = input("Select room type (Regular / Penthouse): ").strip().lower()

        if room_type not in ['regular', 'penthouse']:
            print("Invalid room type. Please choose 'Regular' or 'Penthouse'.")
            return

        available_rooms = get_available_rooms(conn, room_type)
        if not available_rooms:
            print("No available rooms of this type.")
            return

        print(f"\nAvailable {room_type.title()} Rooms:")
        for room in available_rooms:
            print(f"Room ID: {room[0]}, Type: {room[1]}, Cost: ${room[2]}")

        room_id = int(input(f"Enter Room ID from the list above: "))
        start_date = input("Enter start date (YYYY-MM-DD): ")
        end_date = input("Enter end date (YYYY-MM-DD): ")

        start = datetime.strptime(start_date, "%Y-%m-%d")
        end = datetime.strptime(end_date, "%Y-%m-%d")
        if end <= start:
            print("End date must be after start date.")
            return

        if room_type == 'regular':
            cursor.execute("""
                INSERT INTO Reservation (ROOM_ID_REG, ROOM_ID_PENT, BEGINNING_DATE, END_DATE, NAME, EMAIL_ADDRESS)
                VALUES (?, NULL, ?, ?, ?, ?)
            """, (room_id, start_date, end_date, name, email))
        else:
            cursor.execute("""
                INSERT INTO Reservation (ROOM_ID_REG, ROOM_ID_PENT, BEGINNING_DATE, END_DATE, NAME, EMAIL_ADDRESS)
                VALUES (NULL, ?, ?, ?, ?, ?)
            """, (room_id, start_date, end_date, name, email))

        reservation_id = cursor.lastrowid
        conn.commit()
        print(f"Reservation successfully created! Your Reservation ID is: {reservation_id}")

    except sqlite3.IntegrityError as e:
        print(f"Database error: {e}")
    except ValueError as e:
        print(f"Input error: {e}")
    finally:
        conn.close()


def view_reservation():
    #Retrieve an existing reservation
    try:
        reservation_id = int(input("Enter your Reservation ID: "))
        conn = connect_db()
        cursor = conn.cursor()

        # Check both Regular and Penthouse possibilities
        cursor.execute("""
            SELECT r.RESERVATION_NUMBER, r.BEGINNING_DATE, r.END_DATE, r.NAME, r.EMAIL_ADDRESS,
                   reg.COST, reg.TYPE
            FROM Reservation r
            JOIN Regular reg ON r.ROOM_ID_REG = reg.ROOM_ID
            WHERE r.RESERVATION_NUMBER = ?
        """, (reservation_id,))
        result = cursor.fetchone()

        if result:
            print(f"\nReservation Details:")
            print(f"Name: {result[3]}")
            print(f"Email: {result[4]}")
            print(f"Room Type: {result[6]}")
            print(f"Cost: ${result[5]}")
            print(f"Dates: {result[1]} to {result[2]}")
        else:
            # Try Penthouse
            cursor.execute("""
                SELECT r.RESERVATION_NUMBER, r.BEGINNING_DATE, r.END_DATE, r.NAME, r.EMAIL_ADDRESS,
                       p.COST, p.TYPE
                FROM Reservation r
                JOIN Penthouse p ON r.ROOM_ID_PENT = p.ROOM_ID
                WHERE r.RESERVATION_NUMBER = ?
            """, (reservation_id,))
            result = cursor.fetchone()
            if result:
                print(f"\nReservation Details:")
                print(f"Name: {result[3]}")
                print(f"Email: {result[4]}")
                print(f"Room Type: {result[6]}")
                print(f"Cost: ${result[5]}")
                print(f"Dates: {result[1]} to {result[2]}")
            else:
                print("No reservation found with that ID.")
        conn.close()
    except ValueError:
        print("Invalid input. Please enter a numeric Reservation ID.")


def update_reservation():
    #Update name/email on existing reservation
    try:
        reservation_id = int(input("Enter your Reservation ID: "))
        email = input("Enter your email address on file: ").strip()
        new_name = input("Enter new name (or press Enter to keep current): ").strip()
        new_email = input("Enter new email (or press Enter to keep current): ").strip()

        conn = connect_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM Reservation WHERE RESERVATION_NUMBER = ? AND EMAIL_ADDRESS = ?",
                       (reservation_id, email))
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                UPDATE Reservation
                SET NAME = COALESCE(NULLIF(?, ''), NAME),
                    EMAIL_ADDRESS = COALESCE(NULLIF(?, ''), EMAIL_ADDRESS)
                WHERE RESERVATION_NUMBER = ?
            """, (new_name, new_email, reservation_id))
            conn.commit()
            print("Reservation updated successfully.")
        else:
            print("Reservation not found or email mismatch.")

        conn.close()
    except ValueError:
        print("Invalid input. Reservation ID must be a number.")


def cancel_reservation():
    #Delete existing reservation
    try:
        reservation_id = int(input("Enter your Reservation ID: "))
        email = input("Enter your email address on file: ").strip()

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Reservation WHERE RESERVATION_NUMBER = ? AND EMAIL_ADDRESS = ?",
                       (reservation_id, email))
        result = cursor.fetchone()

        if result:
            cursor.execute("DELETE FROM Reservation WHERE RESERVATION_NUMBER = ?", (reservation_id,))
            conn.commit()
            print("Reservation cancelled successfully.")
        else:
            print("Reservation not found or email mismatch.")
        conn.close()
    except ValueError:
        print("Invalid Reservation ID.")


def main_menu():
    #CRUD menu for user
    while True:
        print("\n--- Hotel Reservation System ---")
        print("1. Make a New Reservation")
        print("2. View Reservation Details")
        print("3. Update Reservation Info")
        print("4. Cancel Reservation")
        print("5. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            create_reservation()
        elif choice == '2':
            view_reservation()
        elif choice == '3':
            update_reservation()
        elif choice == '4':
            cancel_reservation()
        elif choice == '5':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")



if __name__ == "__main__":
    main_menu()

