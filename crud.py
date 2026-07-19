# logic of the hotel system

from sqlalchemy.orm import Session
from models import RoomsReservationsValidator, HotelRoomsValidator, AvailableRoomsValidator, CancelReservationsValidator
from database import Hotel, Reservations, CancelReservations
from random import choices
from string import ascii_uppercase, digits

#function for adding hotel to database
def add_hotel_room(db: Session, room_data: HotelRoomsValidator):
    #creating a new variable for room in database
    try:
        new_room = Hotel(**room_data.model_dump())

        #adding to database
        db.add(new_room)
        db.commit()
        #db.refresh(new_room) + return new room | if server answer is meant to be string

        return {"message": "Hotel room has been added succesfully!"}
    except Exception as e:
        db.rollback()
        raise ValueError(f"Failed to add a new room. {e}")

#function for making reservation
def make_reservation(db: Session, reservation_data: RoomsReservationsValidator):
    #creating a new variable to make reservation
    try:
        room = db.query(Hotel).filter(Hotel.room == reservation_data.room_id).first()
        
        if not room:
            raise ValueError(f"Room does not exist.")

        if room.is_taken == "no":
            #creating new reservation
            new_reservation = Reservations(**reservation_data.model_dump())
            #changing status of the room
            room.is_taken = "yes"
            #calculating total price
            total_stay = (reservation_data.check_out_date - reservation_data.check_in_date).days # .days for preventing from timedelta
            #adding new price to database
            if total_stay <= 0:
                raise ValueError(f"You have to stay for at least one full day.")
            
            new_reservation.price = room.price * total_stay
            #adding access code to database
            new_reservation.access_code = ''.join(choices(ascii_uppercase + digits, k=6))
        else:
            raise ValueError(f"This room is already taken. Try to reserve different one!")

        #adding to database
        db.add(new_reservation)
        db.commit()

        return {"message": "Reservation succesfully made! See you soon in tha haul."}
    except Exception as e:
        db.rollback()
        raise ValueError(f"Reservation declinded. {e}")
    
#function for cancelling reservation
def cancel_reservation(db: Session, cancellation_data: CancelReservationsValidator):
    try:
        cancel = db.query(Reservations).filter(Reservations.room_id == cancellation_data.cancel_room_id,
                                               Reservations.guest_name == cancellation_data.guest_name,
                                               Reservations.access_code == cancellation_data.access_code).first()
        
        room = db.query(Hotel).filter(Hotel.ID == cancellation_data.cancel_room_id).first()

        if not cancel:
            raise ValueError(f"Invalid data to cancel reservation.")
        
        if room:
            room.is_taken = "no"

        new_cancellation = CancelReservations(**cancellation_data.model_dump())
        db.add(new_cancellation)
        db.delete(cancel)
        db.commit()

        return {"message": "Reservation succesfully cancelled! Hope you come back soon :)."}
        
    except Exception as e:
        db.rollback()
        raise ValueError(f"Cancellation declined. {e}")

#function for showing available rooms
def show_available_rooms(db: Session, room_data: AvailableRoomsValidator):
    #defining all available rooms 
    overlapping_reservations = db.query(Reservations.room_id).filter(Reservations.check_in_date < room_data.date_to,
                                                                     Reservations.check_out_date > room_data.date_from).all()
    taken_rooms = [reservs[0] for reservs in overlapping_reservations]

    available = db.query(Hotel).filter(Hotel.price >= room_data.over_price,
                                       Hotel.price <= room_data.under_price,
                                       ~Hotel.ID.in_(taken_rooms)).all()
    #looking for rooms in price range 
    if not available:
        return {"message": "No room in this price range or date range."} #different error message -> not user's fault 
    return available