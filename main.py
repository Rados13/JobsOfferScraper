from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session, sessionmaker
from sql_app import crud, models, schemas
from sql_app.database import SessionLocal, engine
from datetime import date
from offer_ordering import start_scrap, scrap
from typing import Dict
from mail import MailSystem
from sql_app.website_names import WebsiteName
from threading import Thread

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


def start_last_scraped(db: Session = get_session_to_start(), scrap_again: bool = False):
    db_date = crud.get_last_scraped_date(db)
    must_scrap = False
    if db_date is None:
        crud.create_last_scraped_date(db, schemas.LastScrapedCreate(**new_last_scraped_date()))
        must_scrap = True
    else:
        db_date = db_date.last_scraped

    if must_scrap or scrap_again or db_date != date.today():
        crud.update_last_scraped_date(db, new_last_scraped_date())
        thread = Thread(target=new_thread_check_updates, args=(db,))
        thread.start()


def new_thread_check_updates(db: Session):
    print("Start scrap")
    new_offers = start_scrap(db)
    if new_offers != 0: mail_system.send_mail_with_new_offers_num(f"Appeared {new_offers} new offers today")
    print("End scrap")


start_last_scraped()


@app.get("/")
async def root(db: Session = Depends(get_db)):
    return {"message": "Hello World"}


@app.get("/offers/{website}")
def read_offers_by_website(website: str, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    start_last_scraped(db)
    for website_enum in WebsiteName:
        if website_enum.value == website:
            return crud.get_offers_by_website_name(db, website_enum, skip=skip, limit=limit)

    raise HTTPException(status_code=404, detail="This website_name doesn't exist")


@app.get("/offers/offer/{offer_id}")
def read_offer(offer_id: int, db: Session = Depends(get_db)):
    start_last_scraped(db)
    db_offer = crud.get_offer(db, offer_id=offer_id)
    if db_offer is None:
        raise HTTPException(status_code=404, detail="This offer doesn't exist")
    return db_offer


@app.get("/offers")
def read_offers(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    start_last_scraped(db)
    return crud.get_offers(db, skip=skip, limit=limit)


"""
@app.get("/scrap/linkedin")
async def scrap_linkedin(db: Session = Depends(get_db)):
    start_last_scraped(db,True)
    return {"work": "Start scrap linkedin"}
"""
