import rooms

#initial set up of tables and data loading:

proj = rooms.Reservations()
proj.reset_database()

reg_reader = rooms.RegularRoom()
reg_reader.read_csv_regular("regular_room.csv")
reg_reader.save_to_db_regular()

pent_reader = rooms.Penthouse()
pent_reader.read_csv_pent("pent_room.csv")
pent_reader.save_to_db_pent()

proj.read_csv_reservation("reservations.csv")
proj.save_to_db_reservation()

# this is a test