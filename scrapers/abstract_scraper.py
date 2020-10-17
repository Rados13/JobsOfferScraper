import abc
from typing import List, Dict
from selenium import webdriver

Vector = List[str]


class OffersScraper(metaclass=abc.ABCMeta):
    offers_links = []

    website_name = None
    text_classes = {}
    logo_class = None
    offers_a_class = None
    next_page_class = None

    def __init__(self, driver):
        self.driver: webdriver = driver
        self.set_up_params()

    @abc.abstractmethod
    def set_up_params(self):
        """
            Setup these params, which are css class of elems
            website_name =
            text_classes = {
                "job_name": [],
                "company_name": [],
                "place": [],
            }
            logo_class = ""
            offers_a_class = ""
            next_page_class = ""
        """

    def get_offers(self) -> List[Dict]:
        offers_links: list = self.get_offers_from_this_page()

        is_end = self.is_next_page_set()
        while is_end:
            offers_links += self.get_offers_from_this_page()
            is_end = self.is_next_page_set()

        return [self.get_offer_data(link) for link in offers_links if link is not None]

    def get_offers_from_this_page(self) -> Vector:
        a_elements = self.driver.find_elements_by_css_selector(self.offers_a_class)
        return [element.get_attribute("href") for element in a_elements]

    def get_offer_data(self, link: str) -> Dict:
        print(f"{self.website_name.value}  {link}")
        self.driver.get(link)
        offer_dict = {key: self.get_text_from_class(value) for key, value in self.text_classes.items()}
        offer_dict['place'] = offer_dict['place'].replace("\n", ",")
        offer_dict['logo_url'] = self.get_logo_src()
        offer_dict['url'] = link
        offer_dict['website_name'] = self.website_name.value
        return offer_dict

    def get_logo_src(self) -> str:
        logo_elem = self.driver.find_elements_by_css_selector(self.logo_class)
        return logo_elem[0].get_attribute("src") if logo_elem else ""

    def get_text_from_class(self, classes_names: List[str]) -> str:
        for class_name in classes_names:
            class_elem = self.driver.find_elements_by_css_selector(class_name)
            if class_elem:
                return class_elem[0].text
        return ""

    def is_next_page_set(self) -> bool:
        a_elements = self.driver.find_elements_by_css_selector(self.next_page_class)
        if a_elements:
            self.driver.get(a_elements[0].get_attribute("href"))
            return True
        return False
