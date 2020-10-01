from typing import List, Dict
from scrapers.abstract_scraper import OffersScraper
from sql_app.website_names import WebsiteName

Vector = List[str]


class PracujScraper(OffersScraper):

    def set_up_params(self):
        self.website_name = WebsiteName.PRACUJ
        self.text_classes = {
            "job_name": [".OfferView1Z5qAH"],
            "company_name": [".OfferViewFf0I7D"],
            "place": [".OfferView3YCkFF", ".OfferViewHbLGvE"],
        }
        self.logo_class = ".OfferView2Jau99"
        self.offers_a_class = ".offer .offer__click-area"
        self.next_page_class = ".pagination_element--next .pagination_trigger"
