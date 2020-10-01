from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from selenium_driver import scrap_data
from typing import List
from fastapi.encoders import jsonable_encoder

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/scrap")
async def start_scrap(db: Session = Depends(get_db)):
    scrapped_offers: List[dict] = scrap_data()
    skip = 0
    db_offers: List[models.Offer] = []
    prev_length = 0
    while True:
        db_offers += crud.get_offers(db, skip)
        skip += 100
        if prev_length == len(db_offers):
            break
        else:
            prev_length = len(db_offers)

    db_offers: List[dict] = [models.Offer.offer_to_dict(offer) for offer in db_offers]
    new_offers = [ scrap_offer for scrap_offer in scrapped_offers if scrap_offer not in db_offers]

    for offer in new_offers:
        crud.create_offer(db, schemas.OfferCreate(**offer))
    return new_offers


@app.get("/offers/{offer_id}")
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    db_offer = crud.get_offer(db, offer_id=offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="This offer doesn't exist")
    return db_offer


@app.get("/offers")
def read_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.get_offers(db, skip=skip, limit=limit)
