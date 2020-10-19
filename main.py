from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from datetime import date
from offer_ordering import start_scrap, scrap
from typing import Dict
from mail import MailSystem
from sql_app.website_names import WebsiteName

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

mail_system = MailSystem()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_session_to_start() -> Session:
    return sessionmaker(bind=engine)()


def new_last_scraped_date() -> Dict:
    return {"last_scraped": date.today()}


def start_last_scraped(db: Session = get_session_to_start()):
    if crud.get_last_scraped_date(db) is None:
        start_scrap(db)
        crud.create_last_scraped_date(db, schemas.LastScrapedCreate(**new_last_scraped_date()))
        print("Start server")


def update_last_scraped(db: Session):
    db_date = crud.get_last_scraped_date(db).last_scraped
    if db_date != date.today():
        new_offers = start_scrap(db)
        crud.update_last_scraped_date(db, new_last_scraped_date())
        if new_offers != 0: mail_system.send_mail_with_new_offers_num(f"Appeared {new_offers} new offers today")


start_last_scraped()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    update_last_scraped(db)
    return {"message": "Hello World"}


@app.get("/scrap/pracuj")
async def scrap_offers():
    return scrap(WebsiteName.PRACUJ)


@app.get("/scrap/linked")
async def scrap_offers():
    return scrap(WebsiteName.LINKEDIN)

@app.get("/scrap/nofluff")
async def scrap_offers():
    return scrap(WebsiteName.NO_FLUFF_JOBS)


@app.get("/offers/{offer_id}")
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    update_last_scraped(db)
    db_offer = crud.get_offer(db, offer_id=offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="This offer doesn't exist")
    return db_offer


@app.get("/offers")
def read_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    update_last_scraped(db)
    return crud.get_offers(db, skip=skip, limit=limit)


@app.get("/offers/{website}")
def read_offers_by_website(website: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    update_last_scraped(db)
    for website_enum in WebsiteName:
        if website_enum.value == website:
            return crud.get_offers_by_website_name(db, website_enum, skip=skip, limit=limit)

    raise HTTPException(status_code=404, detail="This website_name doesn't exist")
