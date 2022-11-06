from fastapi import FastAPI
from app import models
from app.db import engine
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

from app.db import SessionLocal
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from fastapi import Depends
from app import crud

@app.post("/create_address")
def create_address(address:str, db:Session = Depends(get_db)):
    address = crud.create_address(db=db, address=address)
    return {"friend": address}

@app.get("/get_address/{id}/") 
def get_address(id:int, db:Session = Depends(get_db)):
    address = crud.get_address(db=db, id=id)
    return address

@app.get("/list_address")
def list_address(db:Session = Depends(get_db)):
    address_list = crud.list_address(db=db)
    return address_list

@app.put("/update_address/{id}/")
def update_address(id:int, address:str, db:Session=Depends(get_db)):
    db_address = crud.get_address(db=db, id=id)
    if db_address:
        updated_address = crud.update_address(db=db, id=id, address=address)
        return updated_address
    else:
        return {"error": f"address with id {id} does not exist"}


@app.delete("/delete_address/{id}/") 
def delete_address(id:int, db:Session=Depends(get_db)):
    db_address = crud.get_address(db=db, id=id)
    if db_address:
        return crud.delete_address(db=db, id=id)
    else:
        return {"error": f"address with id {id} does not exist"}