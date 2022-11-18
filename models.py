from sqlalchemy import Column, Integer, String, Float

from .db import Base

# model/table
class  addressBook(Base):
    __tablename__ = "addressBook"

    # fields 
    id = Column(Integer,primary_key=True, index=True)
    address = Column(String(50))
    lat = Column(Float)
    # last_name = Column(String(20))
    # age = Column(Integer)