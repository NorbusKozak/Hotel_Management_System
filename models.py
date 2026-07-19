# creating validator using pydantic to counteract wrong hotel reservations

from pydantic import BaseModel, Field, PositiveFloat, PositiveInt
from typing import Literal
from datetime import date

# class for validating Hotel_Rooms
class HotelRoomsValidator(BaseModel):
    floor: int
    room: PositiveInt
    quality: Literal["Standard", "Superior", "Deluxe"]
    sleeps: Literal[1,2,3,4]
    sea_view: Literal["yes", "no"]
    price: float
    is_taken: Literal["yes", "no"]
    

# class for validating Rooms_Reservations
class RoomsReservationsValidator(BaseModel):
    room_id: PositiveInt
    check_in_date: date
    check_out_date: date
    guest_name: str = Field(pattern=r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:\s+[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\-]+)+$")


# class for cancelling reservations
class CancelReservationsValidator(BaseModel):
    cancel_room_id: PositiveInt
    guest_name: str = Field(pattern=r"^[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż]+(?:\s+[A-Za-zĄĆĘŁŃÓŚŹŻąćęłńóśźż\-]+)+$")
    access_code: str


# class for validating available rooms search
class AvailableRoomsValidator(BaseModel):
    over_price: PositiveFloat = Field(default=1.0)
    under_price: PositiveFloat = Field(default=1000.0)
    date_from: date
    date_to: date