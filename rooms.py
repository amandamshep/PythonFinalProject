import db_base as db

reset_db_script = """

DROP TABLE IF EXISTS Regular;

CREATE TABLE Regular(
ROOM_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
TYPE CHAR(7),
COST NUMERIC,
FEATURE_1 TEXT,
FEATURE_2 TEXT,
FEATURE_3 TEXT
);

DROP TABLE IF EXISTS Penthouse;

CREATE TABLE Penthouse (
ROOM_ID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
TYPE CHAR(9),
COST NUMERIC,
FEATURE_1 TEXT,
FEATURE_2 TEXT,
FEATURE_3 TEXT,
FEATURE_4 TEXT,
FEATURE_5 TEXT
);



DROP TABLE IF EXISTS Reservation;

CREATE TABLE Reservation (
    RESERVATION_NUMBER INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    ROOM_ID_REG INTEGER,
    ROOM_ID_PENT INTEGER,
    BEGINNING_DATE DATE NOT NULL,
    END_DATE DATE NOT NULL,
    NAME TEXT,
    EMAIL_ADDRESS TEXT,
    FOREIGN KEY (ROOM_ID_REG) REFERENCES Regular(ROOM_ID),
    FOREIGN KEY (ROOM_ID_PENT) REFERENCES Penthouse(ROOM_ID)
);


CREATE TRIGGER prevent_overlap_regular
BEFORE INSERT ON Reservation
WHEN NEW.ROOM_ID_REG IS NOT NULL
BEGIN
    SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1 FROM Reservation
            WHERE ROOM_ID_REG = NEW.ROOM_ID_REG
              AND (
                    (NEW.BEGINNING_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (NEW.END_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (BEGINNING_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
                 OR (END_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
              )
        )
        THEN RAISE(ABORT, 'Conflict: Overlapping dates for regular room.')
    END;
END;


CREATE TRIGGER prevent_overlap_penthouse
BEFORE INSERT ON Reservation
WHEN NEW.ROOM_ID_PENT IS NOT NULL
BEGIN
    SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1 FROM Reservation
            WHERE ROOM_ID_PENT = NEW.ROOM_ID_PENT
              AND (
                    (NEW.BEGINNING_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (NEW.END_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (BEGINNING_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
                 OR (END_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
              )
        )
        THEN RAISE(ABORT, 'Conflict: Overlapping dates for penthouse room.')
    END;
END;


CREATE TRIGGER prevent_overlap_regular_update
BEFORE UPDATE ON Reservation
WHEN NEW.ROOM_ID_REG IS NOT NULL
BEGIN
    SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1 FROM Reservation
            WHERE ROOM_ID_REG = NEW.ROOM_ID_REG
              AND RESERVATION_NUMBER != OLD.RESERVATION_NUMBER
              AND (
                    (NEW.BEGINNING_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (NEW.END_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (BEGINNING_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
                 OR (END_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
              )
        )
        THEN RAISE(ABORT, 'Conflict: Overlapping dates for regular room.')
    END;
END;


CREATE TRIGGER prevent_overlap_penthouse_update
BEFORE UPDATE ON Reservation
WHEN NEW.ROOM_ID_PENT IS NOT NULL
BEGIN
    SELECT 
    CASE
        WHEN EXISTS (
            SELECT 1 FROM Reservation
            WHERE ROOM_ID_PENT = NEW.ROOM_ID_PENT
              AND RESERVATION_NUMBER != OLD.RESERVATION_NUMBER
              AND (
                    (NEW.BEGINNING_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (NEW.END_DATE BETWEEN BEGINNING_DATE AND END_DATE)
                 OR (BEGINNING_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
                 OR (END_DATE BETWEEN NEW.BEGINNING_DATE AND NEW.END_DATE)
              )
        )
        THEN RAISE(ABORT, 'Conflict: Overlapping dates for penthouse room.')
    END;
END;



"""

class RegularRoom(db.DBbase):
    def __init__(self):
        pass

    def add_regular(self):
        try:
            sql = """
            
            """
            super().get_cursor.execute(sql)
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def update_regular(self):
        try:
            sql = """

                        """
            super().get_cursor.execute(sql)
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def delete_regular(self):
        try:
            sql = """

                        """
            super().get_cursor.execute(sql)
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def fetch_regular(self):
        try:
            pass
        except Exception as e:
            print("An error occurred.", e)

class Penthouse(RegularRoom):
    def add_pent(self):
        try:
            sql = """

            """
            super().get_cursor.execute(sql)
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def fetch_pent(self):
        try:
            pass
        except Exception as e:
            print("An error occurred.", e)

class Reservations(db.DBbase):
    def __init__(self):
        super(Reservations, self).__init__("HotelReservations.sqlite")

    def reset_database(self):
        try:
            sql = reset_db_script
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred.", e)
        finally:
            super().close_db()

    def add_reservation(self, beg_date, end_date, name, email, room_id_reg = None, room_id_pent=None):
        try:
            sql = """
                INSERT INTO Reservation (ROOM_ID_REG, ROOM_ID_PENT, BEGINNING_DATE, END_DATE, NAME, EMAIL_ADDRESS)
                VALUES (?,?,?,?,?,?);
            """
            super().get_cursor.execute(sql, (room_id_reg, room_id_pent, beg_date, end_date, name, email))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def update_reservation(self, name, email, beg_date, end_date, reservation_number):
        try:
            sql = """
                UPDATE Reservation
                SET 
                    NAME = ?,
                    EMAIL_ADDRESS = ?,
                    BEGINNING_DATE = ?,
                    END_DATE = ?
                WHERE RESERVATION_NUMBER = ?;
                        """
            super().get_cursor.execute(sql, (name, email, beg_date, end_date, reservation_number))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def delete_reservation(self, reservation_number):
        try:
            sql = """
                DELETE FROM Reservation
                WHERE Reservation_Number = ?;
                """
            super().get_cursor.execute(sql, (reservation_number,))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred.", e)

    def fetch_reservation(self, reservation_number):
        try:
            return super().get_cursor.execute("SELECT * FROM Reservation WHERE Reservation_Number = ?;", (reservation_number,)).fetchone()
        except Exception as e:
            print("An error occurred.", e)