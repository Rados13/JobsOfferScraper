from scrapers.abstract_scraper import OffersScraper
from typing import Dict, List
from time import sleep
from selenium.common.exceptions import WebDriverException
from sql_app.website_names import WebsiteName


class LinkedInScraper(OffersScraper):
    def set_up_params(self):
        self.website_name = WebsiteName.LINKEDIN
        self.text_classes = {
            "job_name": [".topcard__title"],
            "company_name": [".topcard__org-name-link", ".topcard__flavor"],
            "place": [".topcard__flavor--bullet"],
        }
        self.logo_class = ".company-logo"
        self.offers_a_class = ".result-card__full-card-link"
        self.next_page_class = ".infinite-scroller__show-more-button"

    def get_offers(self) -> List[Dict]:
        self.wait_for_load_page()
        is_end = self.is_next_page_set()
        offers_links: list = self.get_offers_from_this_page()
        while is_end:
            offers_links += self.get_offers_from_this_page()[len(offers_links):]
            is_end = self.is_next_page_set()

        return [self.get_offer_data(link) for link in offers_links]

    def is_next_page_set(self) -> bool:
        li_elements = self.driver.find_elements_by_css_selector(self.next_page_class)

        old_height = -1
        new_height = 0

        while new_height != old_height:
            old_height = new_height
            new_height = self.driver.execute_script(
                """
                    window.scrollTo(0, document.body.scrollHeight); 
                    return document.body.scrollHeight;
                """)
            sleep(2)

        is_end = False
        if li_elements:
            try:
                li_elements[0].click()
                is_end = True
            except WebDriverException:
                is_end = False
        return is_end
