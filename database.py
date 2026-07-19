from sqlalchemy import create_engine, Column, String, Float, Integer, ForeignKey, DateTime, Date
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime

engine = create_engine('sqlite:///hotel.db', echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class Hotel(Base):
    __tablename__ = "Hotel_Rooms"   
    ID = Column(Integer, primary_key=True)
    floor = Column(Integer)
    room = Column(Integer, unique=True)
    quality = Column(String)
    sleeps = Column(Integer)
    sea_view = Column(String)
    price = Column(Float)
    is_taken = Column(String)


class Reservations(Base):
    __tablename__ = "Rooms_Reservations"
    ID = Column(Integer, primary_key=True)
    room_id = Column(Integer, ForeignKey("Hotel_Rooms.ID"))
    check_in_date = Column(Date)
    check_out_date = Column(Date)
    guest_name = Column(String)
    price = Column(Float)
    access_code = Column(String)

class CancelReservations(Base):
    __tablename__ = "Cancel_Reservations"
    ID = Column(Integer, primary_key=True)
    cancel_room_id = Column(Integer, ForeignKey("Hotel_Rooms.ID"))
    guest_name = Column(String)
    cancellation_date = Column(DateTime, default=datetime.utcnow) #checking the date here (not giving user option to write date)
    access_code = Column(String)
