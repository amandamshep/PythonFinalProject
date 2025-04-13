import db_base as db
import csv

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

class Reservations(db.DBbase):
    def __init__(self):
        self.res_list = []
        super(Reservations, self).__init__("HotelReservations.sqlite")

    def reset_database(self):
        try:
            sql = reset_db_script
            super().execute_script(sql)
        except Exception as e:
            print("An error occurred in reset_database.", e)
        # finally:
        #     super().close_db()

    def add_reservation(self, start_date, end_date, name, email, room_id_reg = None, room_id_pent=None):
        try:
            if room_id_reg == "0":
                sql = """
                        INSERT INTO Reservation (ROOM_ID_REG, ROOM_ID_PENT, BEGINNING_DATE, END_DATE, NAME, EMAIL_ADDRESS)
                        VALUES (NULL,?,?,?,?,?);
                    """
                super().get_cursor.execute(sql, (room_id_pent, start_date, end_date, name, email))
                print(room_id_reg, room_id_pent, start_date, end_date, name, email)
            if room_id_pent == "0":
                sql = """
                        INSERT INTO Reservation (ROOM_ID_REG, ROOM_ID_PENT, BEGINNING_DATE, END_DATE, NAME, EMAIL_ADDRESS)
                        VALUES (?,NULL,?,?,?,?);
                    """
                super().get_cursor.execute(sql, (room_id_reg, start_date, end_date, name, email))
                print(room_id_reg, room_id_pent, start_date, end_date, name, email)
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred in add_reservation.", e)

    def update_reservation(self, name, email, start_date, end_date, reservation_number):
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
            super().get_cursor.execute(sql, (name, email, start_date, end_date, reservation_number))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred in update_reservation.", e)

    def delete_reservation(self, reservation_number):
        try:
            sql = """
                DELETE FROM Reservation
                WHERE Reservation_Number = ?;
                """
            super().get_cursor.execute(sql, (reservation_number,))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred in delete_reservation.", e)

    def fetch_reservation(self, reservation_number):
        try:
            return super().get_cursor.execute("SELECT * FROM Reservation WHERE Reservation_Number = ?;", (reservation_number,)).fetchone()
        except Exception as e:
            print("An error occurred in fetch_reservation.", e)

    def read_csv_reservation(self, filename):
        self.res_list = []
        try:
            with (open(filename, 'r') as record):
                csv_contents = csv.reader(record)
                next(record)  # skip headers
                for row in csv_contents:
                    res = { "name": row[0],
                            "email": row[1],
                            "start_date": row[2],
                            "end_date": row[3],
                            "room_id_reg": row[4],
                            "room_id_pent": row[5],
                            }
                    self.res_list.append(res)
        except Exception as e:
            print("An error occurred in read_csv_reservations.", e)

    def save_to_db_reservation(self):
        for res in self.res_list:
            try:
                self.add_reservation(res['start_date'], res['end_date'], res['name'], res['email'], res['room_id_reg'], res['room_id_pent'])
            except Exception as e:
                print("An error occurred in save_to_db_reservation.", e)

    def get_available_rooms_for_dates(self):
        pass


class RegularRoom(Reservations):
    def __init__(self):
        self.regular_list = []
        super(Reservations, self).__init__("HotelReservations.sqlite")

    def add_regular(self, room_type, cost, f1, f2, f3):
        try:
            sql = """
            INSERT INTO Regular (TYPE, COST, FEATURE_1, FEATURE_2, FEATURE_3)  
            VALUES (?, ?, ?, ?, ?);
            """
            super().get_cursor.execute(sql, (room_type, cost, f1, f2, f3))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred in add_regular.", e)


    def fetch_regular(self, room_id):
        try:
            return super().get_cursor.execute("SELECT * FROM Regular WHERE ROOM_ID = ?;", (room_id,)).fetchone()
        except Exception as e:
            print("An error occurred in fetch_regular.", e)

    def read_csv_regular(self, filename):
        self.regular_list = []
        try:
            with open(filename, 'r') as record:
                csv_contents = csv.reader(record)
                next(record)  # skip headers
                for row in csv_contents:
                    reg = {
                        "room_type": row[0],
                        "cost": row[1],
                        "f1": row[2],
                        "f2": row[3],
                        "f3": row[4]
                    }
                    self.regular_list.append(reg)
        except Exception as e:
            print("An error occurred in read_csv_regular.", e)

    def save_to_db_regular(self):
        for room in self.regular_list:
            try:
                self.add_regular(room['room_type'], room['cost'], room['f1'],room['f2'],room['f3'])
            except Exception as e:
                print("An error occurred in save_to_db_regular.",e)

class Penthouse(RegularRoom):
    def __init__(self):
        super(Reservations, self).__init__("HotelReservations.sqlite")
        self.pent_list = []


    def add_pent(self, room_type, cost, f1, f2, f3, f4, f5):
        try:
            sql = """
                INSERT INTO Penthouse (TYPE, COST, FEATURE_1, FEATURE_2, FEATURE_3, FEATURE_4, FEATURE_5)  
                VALUES (?, ?, ?, ?, ?, ?,?);

            """
            super().get_cursor.execute(sql, (room_type, cost, f1, f2, f3, f4, f5))
            super().get_connection.commit()
        except Exception as e:
            print("An error occurred in add_pent.", e)

    def fetch_pent(self, room_id):
        try:
            return super().get_cursor.execute("SELECT * FROM Regular WHERE ROOM_ID = ?;", (room_id,)).fetchone()
        except Exception as e:
            print("An error occurred in fetch_pent.", e)

    def read_csv_pent(self, filename):
        self.pent_list = []
        try:
            with (open(filename, 'r') as record):
                csv_contents = csv.reader(record)
                next(record)  # skip headers
                for row in csv_contents:
                    pent = { "room_type" : row[0],
                             "cost": row[1],
                             "f1": row[2],
                             "f2": row[3],
                             "f3": row[4],
                             "f4": row[5],
                             "f5": row[6],
                             }
                    self.pent_list.append(pent)
        except Exception as e:
            print("An error occurred in read_csv_pent.", e)

    def save_to_db_pent(self):
        for room in self.pent_list:
            try:
                self.add_pent(room['room_type'], room['cost'], room['f1'],room['f2'],room['f3'], room['f4'], room['f5'])
            except Exception as e:
                print("An error occurred in save_to_db_pent.", e)



