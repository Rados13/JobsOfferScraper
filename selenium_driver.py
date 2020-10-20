from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.pracuj_scraper import PracujScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.nofluffjobs_scraper import NoFluffJobsScrapper
from typing import List, Dict
from sql_app.website_names import WebsiteName
import os


def start_driver():
    # """
    # Setup for heroku
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--disable-gpu")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), options=chrome_options)
    # """

    """
    # Setup for local
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    """
    return driver


driver = start_driver()


def scrap(website_name: WebsiteName) -> List[Dict]:
    return {
        WebsiteName.NO_FLUFF_JOBS: scrap_nofluff_jobs,
        WebsiteName.PRACUJ: scrap_pracuj,
        WebsiteName.LINKEDIN: scrap_linkedin
    }[website_name]()


def scrap_linkedin() -> List[Dict]:
    driver.get(os.environ.get("linkedin_url"))
    # driver.get("https://www.linkedin.com/jobs/search?keywords=IT&location=Krak%C3%B3w%2C%2BWoj.%2BMa%C5%82opolskie%2C%2BPolska&geoId=103263110&trk=public_jobs_jobs-search-bar_search-submit&f_E=2&redirect=false&position=1&pageNum=0")
    return LinkedInScraper(driver).get_offers()


def scrap_pracuj() -> List[Dict]:
    # driver.get("https://www.pracuj.pl/praca/krakow-x44-katowice;wp?rd=30&cc=5013005%2c5015%2c5016&et=1")
    driver.get(os.environ.get("pracuj_url"))
    return PracujScraper(driver).get_offers()


def scrap_nofluff_jobs() -> List[Dict]:
    # driver.get("https://nofluffjobs.com/pl/jobs/krakow?criteria=city%3Dkrakow,slask%20seniority%3Dtrainee&page=1")
    # driver.get("https://nofluffjobs.com/pl/jobs/krakow?criteria=city%3Dkrakow,slask%20seniority%3Dtrainee,junior&page=1")
    driver.get(os.environ.get("nofluff_jobs_url"))
    return NoFluffJobsScrapper(driver).get_offers()
