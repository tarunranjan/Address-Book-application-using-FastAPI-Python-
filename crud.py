from sqlalchemy.orm import Session
from app.models import addressBook


def create_address(db:Session, address):
    new_address = addressBook(address=address)
    db.add(new_address)
    db.commit()
    db.refresh(new_address)
    return new_address

def get_address(db:Session, id:int):
    db_addresbook = db.query(addressBook).filter(addressBook.id==id).first()
    return db_addresbook

def list_address(db:Session):
    all_address = db.query(addressBook).all()
    return all_address


def update_address(db:Session, id:int, address: str):
    db_address = get_address(db=db, id=id)
    db_address.address = address
    db.commit()
    db.refresh(db_address) 
    return db_address

def delete_address(db:Session, id:int):
    db_address = get_address(db=db, id=id)
    db.delete(db_address)
    db.commit() 