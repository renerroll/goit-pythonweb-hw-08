from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contacts_api.database import engine, SessionLocal
from contacts_api import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
async def read_root():
    return {"message": "Welcome to the database"}

@app.post("/contacts/", response_model=schemas.ContactOut)
def create_contact(contact: schemas.ContactCreate, db: Session = Depends(get_db)):
    return crud.create_contact(db, contact)

@app.get("/contacts_api", response_model=list[schemas.ContactOut])
def read_contacts(db: Session = Depends(get_db)):
    return crud.get_contacts(db)

@app.get("/contacts/{contact_id}", response_model=schemas.ContactOut)
def read_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = crud.get_contact_by_id(db, contact_id)
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=schemas.ContactOut)
def update_contact(contact_id: int, contact: schemas.ContactUpdate, db: Session = Depends(get_db)):
    update_contact = crud.update_contact(db, contact_id, contact)
    if not update_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return update_contact

@app.delete("/contacts/{contact_id}", response_model=schemas.ContactOut)
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    delete_contact = crud.delete_contact(db, contact_id)
    if not delete_contact:
        raise HTTPException(status_code=404, detail="Contact not found")
    return delete_contact

@app.get("/contacts/search/")
def search_contacts(query: str, db: Session = Depends(get_db)):
    contacts = crud.search_contacts(db, query)
    return contacts

@app.get("/contacts/birthdays/", response_model=list[schemas.ContactOut])
def upcoming_birthdays(db: Session = Depends(get_db)):
    return crud.get_upcoming_birthdays(db)