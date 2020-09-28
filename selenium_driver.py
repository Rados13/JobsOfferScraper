from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from scrapers.pracuj_scraper import PracujScraper
from typing import List

"""
Setup for heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")
driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
"""

"""
Setup for local
"""


# driver.get("https://www.pracuj.pl/praca/krakow;wp?rd=30&cc=5013005%2c5015%2c5016&et=1%2c17%2c18")
# result = PracujScraper(driver).get_offers()
# print(len(result))

def scrap_data() -> List[dict]:
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get("https://www.pracuj.pl/praca/krakow-x44-katowice;wp?rd=30&cc=5013005%2c5015%2c5016&et=1")
    return PracujScraper(driver).get_offers()
