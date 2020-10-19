from pydantic import BaseModel
from datetime import date


class OfferBase(BaseModel):
    job_name: str
    company_name: str
    website_name: str
    place: str
    found_date: date = date.today()
    logo_url: str = None
    url: str


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        orm_model = True


class LastScrapedBase(BaseModel):
    last_scraped: date


class LastScrapedCreate(LastScrapedBase):
    pass


class LastScraped(LastScrapedBase):
    id: int

    class Config:
        orm_model = True
