from sqlalchemy import Column, Integer, String, Date
from sql_app.database import Base
from typing import Dict
from datetime import date


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String, index=True)
    company_name = Column(String)
    website_name = Column(String, index=True)
    place = Column(String)
    logo_url = Column(String, nullable=True)
    url = Column(String)
    found_date = Column(Date, index=True, default=date.today())

    @staticmethod
    def offer_to_comparable_dict(elem) -> Dict:
        return {
            "job_name": elem.job_name,
            "company_name": elem.company_name,
            "place": elem.place,
            "logo_url": elem.logo_url,
            "url": elem.url,
            "website_name": elem.website_name,
        }


class LastScraped(Base):
    __tablename__ = "last_scraped"

    id = Column(Integer, primary_key=True, index=True)
    last_scraped = Column(Date)
