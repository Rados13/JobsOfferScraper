from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app import crud, models, schemas
from selenium_driver import scrap
from typing import List, Dict
from sql_app.website_names import WebsiteName


def start_scrap(db: Session) -> int:
    new_offers_amount = 0
    for website in WebsiteName:
        scrapped_offers: List[Dict] = scrap(website)
        new_offers, expired_offers = get_new_and_expired_offers(db, website, scrapped_offers)
        for offer in new_offers:
            crud.create_offer(db, schemas.OfferCreate(**offer))
        for offer in expired_offers:
            crud.delete_offer(db, offer.id)
        new_offers_amount += len(new_offers)

    return new_offers_amount


def get_new_and_expired_offers(db: Session, website: WebsiteName, scrapped_offers: List[Dict]) -> (
        List[Dict], List[Dict]):
    skip = 0
    ended_offers = []
    while True:
        db_offers = crud.get_offers_by_website_name(db, website, skip)
        if len(db_offers) == 0:
            return scrapped_offers, ended_offers

        for old_offer in db_offers:
            old_offer_dict = models.Offer.offer_to_comparable_dict(old_offer)
            idx = find_index_or_none(scrapped_offers, old_offer_dict)
            if idx is None:
                ended_offers.append(old_offer)
            else:
                scrapped_offers.pop(idx)
        skip += 100


def find_index_or_none(some_list: List, potential_elem):
    idx = 0
    for elem in some_list:
        if elem == potential_elem:
            return idx
        else:
            idx += 1
    return None


def get_all_offers(db: Session) -> List[Dict]:
    db_offers = []
    skip = 0
    while True:
        next_offers = crud.get_offers(db, skip)
        db_offers += next_offers
        skip += 100
        if len(db_offers) == 0:
            break
    return db_offers
