from scrapers.abstract_scraper import OffersScraper
from sql_app.website_names import WebsiteName


class NoFluffJobsScrapper(OffersScraper):
    def set_up_params(self):
        self.website_name = WebsiteName.NO_FLUFF_JOBS
        self.text_classes = {
            "job_name": [".posting-details-description h1"],
            "company_name": [".posting-details-description a dl dd"],
            "place": [".locations-compact li"],
        }
        self.logo_class = ".posting-logo img"
        self.offers_a_class = ".posting-list-item"
        self.next_page_class = ".page-link"

    def is_next_page_set(self) -> bool:
        url = self.driver.current_url

        a_elements = self.driver.find_elements_by_css_selector(self.next_page_class)
        is_end = False
        if a_elements:
            next_a_element = a_elements[-1:][0]
            link, num = self.get_page_num(url)
            if not next_a_element.get_attribute("aria-disabled"):
                link += f"page={num + 1}"
                self.driver.get(link)
                is_end = True

        return is_end

    def get_page_num(self, url: str) -> (str, int):
        link, num, *rest = url.split("page=")
        return link, int(num)


