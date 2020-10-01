from typing import List
from scrapers.abstract_scraper import OffersScraper

Vector = List[str]


class PracujScraper(OffersScraper):
    text_classes = {
        "job_name": ["OfferView1Z5qAH"],
        "company_name": ["OfferViewFf0I7D"],
        "place": ["OfferView3YCkFF", "OfferViewHbLGvE"],
        # "employment_type": ["OfferView3YCkFF"],
        "when_end": ["OfferView1YEokC"]
    }
    logo_class = "OfferView2Jau99"

    def get_offers(self) -> List[dict]:
        offers_links: list = self.get_offers_from_this_page()
        next_page = self.get_next_page_link()
        while next_page:
            self.driver.get(next_page)
            offers_links += self.get_offers_from_this_page()
            next_page = self.get_next_page_link()

        return [self.get_offer_data(link) for link in offers_links]

    def get_offers_from_this_page(self) -> Vector:
        a_elements = self.driver.find_elements_by_css_selector(".offer .offer__click-area")
        return [element.get_attribute("href") for element in a_elements]

    def get_offer_data(self, link: str) -> dict:
        self.driver.get(link)
        offer_dict = {key: self.get_text_from_class(value) for key,value in self.text_classes.items()}
        logo_elem = self.driver.find_elements_by_css_selector(f".{self.logo_class}")
        offer_dict['logo_url'] = logo_elem[0].get_attribute("src") if logo_elem else ""
        offer_dict['url'] = link
        return offer_dict

    def get_text_from_class(self, classes_names: List[str]) -> str:
        for class_name in classes_names:
            class_elem = self.driver.find_elements_by_css_selector(f".{class_name}")
            if class_elem:
                return class_elem[0].text
        return ""

    def get_next_page_link(self):
        a_elements = self.driver.find_elements_by_css_selector(".pagination_element--next .pagination_trigger")
        return a_elements[0].get_attribute("href") if a_elements else ""
