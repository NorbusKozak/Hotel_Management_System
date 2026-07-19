from fastapi import FastAPI, Depends, HTTPException
from crud import add_hotel_room, make_reservation, show_available_rooms, cancel_reservation
from  models import RoomsReservationsValidator, HotelRoomsValidator, AvailableRoomsValidator, CancelReservationsValidator
from database import get_db, engine, Base
from sqlalchemy.orm import Session

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Welcome in Gucio Hotel")

#endpoint for creating a room
@app.post('/create_room')
def create_hotel_room(room: HotelRoomsValidator, db: Session = Depends(get_db)):
    try:    
        new_room = add_hotel_room(db=db, room_data=room)
        return new_room
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    
#endpoint for making a reservation
@app.post('/make_reservation')
def reserve_room(reservation: RoomsReservationsValidator, db: Session = Depends(get_db)):
    try:
        new_reservation = make_reservation(db=db, reservation_data=reservation)
        return new_reservation
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#endpoint for cancelling a reservation
@app.post('/cancel_reservation')
def cancel_room(cancel_room: CancelReservationsValidator, db: Session = Depends(get_db)):
    try:
        new_cancel = cancel_reservation(db=db, cancellation_data=cancel_room)
        return new_cancel
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

#endpoint for available rooms
@app.get('/show_available_rooms')
def available_rooms(available_room: AvailableRoomsValidator = Depends(), db: Session = Depends(get_db)):
    try:
        room = show_available_rooms(db=db, room_data=available_room)
        return room
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))