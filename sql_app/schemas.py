from pydantic import BaseModel


class OfferBase(BaseModel):
    job_name: str
    company_name: str
    place: str
    when_end: str
    logo_url: str
    url: str


class OfferCreate(OfferBase):
    pass


class Offer(OfferBase):
    id: int

    class Config:
        orm_model = True
