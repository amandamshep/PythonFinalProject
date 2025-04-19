
#initial set up of tables and data loading:
proj = rooms.Reservations()
proj.reset_database()

# Load regular room data into database
reg = rooms.RegularRoom()
reg.read_csv_regular("regular_room.csv")
reg.save_to_db_regular()  

# Load penthouse room data into database
pent = rooms.Penthouse()
pent.read_csv_pent("pent_room.csv")
pent.save_to_db_pent()

# Load reservation data into database
res = rooms.Reservations()
res.read_csv_reservation("reservations.csv")
res.save_to_db_reservation()

# Failed because room was already reserved which is what we want.
#reg.update_regular(room_id=1, cost=100,f1= "5 queen bed")

# Code worked and the cost of the room was sucessfully updated to 100 dollars with f1 at 5 Queen Bed instead of 2 Queen Bed
# reg.update_regular(room_id=4, cost=100,f1= "5 queen bed")

# # Reupdated room back to old conditions
# reg.update_regular(room_id=4,cost=200,f1 = "2 Queen Bed")

# # Update all the conditions of a room
# reg.update_regular(room_id=4,cost=400,f1="3 Queen Bed",f2="Extra Large Bathroom",f3="small fridge")

# # Revert back to original features
# reg.update_regular(room_id=4,cost=200,f1="2 Queen Bed",f2="Standard Bathroom",f3="Single-serve coffee maker")

# Delete a room, failed, since there is a reservation for this room. 
# reg.delete_regular(10)
# Will Work, since there is no reservation for this room
# reg.delete_regular(4)


# pent = rooms.Penthouse()
# Failed, since it already has a reservation. This is the expected behavior.
# pent.update_pent(room_id=1,cost=400,f3=" Premium Hot Tub")

# Failed, since there is already a reservation, this is the expected behavior.
# pent.delete_pent(2)

# Succeeded, since there are no reservations for the room.
# pent.update_pent(room_id=20,f3="Premium Hot Tub")

# Succeeded, since there are no reservations for the room.
# pent.delete_pent(room_id =19)
