from fastapi import FastAPI, Depends
from pydantic import BaseModel,  types

from typing import Optional, List
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from sqlalchemy import Boolean, Column, Float, String, Integer
import requests
from math import sin, cos, sqrt, atan2
import geopy.distance

app = FastAPI()

# SqlAlchemy Setup
SQLALCHEMY_DATABASE_URL = 'sqlite:///./app.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True, future=True,connect_args={'check_same_thread': False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# A SQLAlchemny ORM Place
class DBPlace(Base):
    __tablename__ = 'places'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
   
    lat = Column(Float)
    lng = Column(Float)

Base.metadata.create_all(bind=engine)

# A Pydantic Place
class Place(BaseModel):
    name: str
    lat: float
    lng: float

    class Config:
        orm_mode = True

# Methods for interacting with the database

def new_get_place(db: Session, lat:float,lng:float):
    return db.query(DBPlace).where(DBPlace.lat==lat,DBPlace.lng ==lng).first()

def get_place(db: Session, place_id: int):
    return db.query(DBPlace).where(DBPlace.id == place_id).first()

def get_places(db: Session):
    return db.query(DBPlace).all()

def create_place(db: Session, place: Place):
    db_place = DBPlace(**place.dict())
    db.add(db_place)
    db.commit()
    db.refresh(db_place)

    return db_place

# Routes for interacting with the API
@app.post('/places/', response_model=Place)
def create_places_view(place: Place, db: Session = Depends(get_db)):
    db_place = create_place(db, place)
    return db_place

@app.get('/places/', response_model=List[Place])
def get_places_view(db: Session = Depends(get_db)):
    return get_places(db)

@app.get('/place/{place_id}')
def get_place_view(place_id: int, db: Session = Depends(get_db)):
    return get_place(db, place_id)

@app.get('/')
async def root():
    return {'message': 'Hello World!'}


@app.get('/place/')
def get_place_view(lat: float,lng:float, db: Session = Depends(get_db)):
    return new_get_place(db, lat,lng)

@app.get('/test')
def get_range(range:int):
    var = requests.get(url = "http://localhost:8000/places/")
    data = var.json()
    return get_range(range)

  
  



