import abc
from typing import List

Vector = List[str]


class OffersScraper(metaclass=abc.ABCMeta):
    offers_links = []

    def __init__(self, driver):
        self.driver = driver

    @abc.abstractmethod
    def get_offers(self) -> List[dict]:
        """
            Get all offers links from all pages
        """

    @abc.abstractmethod
    def get_offers_from_this_page(self) -> str:
        """
            Get offers links from current page
        """

    @abc.abstractmethod
    def get_offer_data(self, link: str) -> dict:
        """
            Get offer data structure from all offers_links
        """

    @abc.abstractmethod
    def get_next_page_link(self) -> str:
        """
            Get next page link
        """
