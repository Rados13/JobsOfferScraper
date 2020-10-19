from sqlalchemy.orm import Session
from sqlalchemy import update
from typing import Dict
from sql_app import schemas, models
from sql_app.website_names import WebsiteName
from datetime import date


def get_offer(db: Session, offer_id: int):
    return db.query(models.Offer).filter(models.Offer.id == offer_id).first()


def get_offers(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).offset(skip).limit(limit).all()


def get_offers_by_website_name(db: Session, website_name: WebsiteName, skip: int = 0, limit: int = 100):
    return db.query(models.Offer).filter(models.Offer.website_name == website_name.value).offset(skip).limit(
        limit).all()


def update_offer(db: Session, offer_id: int, new_offer: Dict):
    db.query(models.Offer).filter(models.Offer.id == offer_id).update(new_offer, synchronize_session=False)
    db.commit()


def delete_offer(db: Session, offer_id: int):
    db.query(models.Offer).filter(models.Offer.id == offer_id).delete()
    db.commit()


def create_offer(db: Session, offer: schemas.OfferCreate):
    db_offer = models.Offer(**offer.dict())
    db.add(db_offer)
    db.commit()
    db.refresh(db_offer)
    return db_offer


def get_last_scraped_date(db: Session):
    return db.query(models.LastScraped).first()


def update_last_scraped_date(db: Session, new_scraped: Dict):
    db.query(models.LastScraped).update(new_scraped, synchronize_session=False)
    db.commit()


def create_last_scraped_date(db: Session, last_scraped: schemas.LastScrapedCreate):
    db_last_scraped = models.LastScraped(**last_scraped.dict())
    db.add(db_last_scraped)
    db.commit()
    db.refresh(db_last_scraped)
    return db_last_scraped
