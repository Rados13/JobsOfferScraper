from sqlalchemy import Column, Integer, String
from sql_app.database import Base


class Offer(Base):
    __tablename__ = "offers"

    id = Column(Integer, primary_key=True, index=True)
    job_name = Column(String)
    company_name = Column(String)
    place = Column(String)
    when_end = Column(String)
    logo_url = Column(String)
    url = Column(String)

    # def __init__(self, job_name: str, place: str, when_end: str, company_name, logo_url: str,url:str):
    #     self.job_name = job_name
    #     self.place = place
    #     self.when_end = when_end
    #     self.logo_url = logo_url
    #     self.company_name = company_name
    #     self.url = url

    @staticmethod
    def offer_to_dict(elem) -> dict:
        return {
            "job_name": elem.job_name,
            "company_name": elem.company_name,
            "place": elem.place,
            "when_end": elem.when_end,
            "logo_url": elem.logo_url,
            "url": elem.url
        }


