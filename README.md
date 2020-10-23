# Jobs Offer Scraper

![made-with-python](https://img.shields.io/badge/Main%20language-Python-Green)

### What is it?

Jobs offer scraper is web application. 
It scrap intern offers from these three pages ([pracuj.pl](https://www.pracuj.pl/), 
[linkdein](https://www.linkedin.com), [nofluffjobs](https://nofluffjobs.com/pl/jobs)).
Storage it on database. Send how many new offers appears these day to my mail.
It also check if offer still appear on the page and if not delete it from database.
It is deployed on heroku. [page-link](https://job-offers-scraper.herokuapp.com/).
To gurantee every day update i use [cron-job](https://cron-job.org).

---

### Technologies
* Python 
* FastAPI (RestAPI server)
* Selenium (Library for scraping data)
* PostgresSQL (Database)
* SqlAlchemy (Database mapper)

---

### TODO Features
* Adding next pages to scrap
* Adding new table for company
* Extend API on query company_name, job_name etc.

---

### Database Scheme
---
#### Tables:
  * offers
  * last_scraped
---
 
#### Fields in collections:

  * Offers:
    * id (int)
    * job_name (string) - job title, ex software engineer
    * company_name (string) - which company offer this job
    * website_name (string) - on which page it was found 
    * place (string) - localization of job
    * logo_url (string) - url of company logo
    * url (string) - url to this offer on website
    * found_date (Date) - date when this offer was found
    ---
  * last_scraped:
    * id (int)
    * last_scraped (Date) - date when last scraping was made. 
    Something like system variable to prevent more than one scraping per day.

### Files:

* [main](main.py) - file where fastapi server was setup 
* [offer_ordering](offer_ordering.py) - connector between database and scraped data
* [mail](mail.py) - class responsible for sending mails
* [selenium_driver](selenium_driver.py) - file with selenium webdriver and calling specified Scraper
* [scrapers](scrapers) - package where are all classes related to scraping data from specific page
    * [abstract_scraper](scrapers/abstract_scraper.py) - class with common code for all scraper classes
    * [linkedin_scraper](scrapers/linkedin_scraper.py) - class for scraping data from linkedin
    * [nofluffjobs_scraper](scrapers/nofluffjobs_scraper.py) - class for scraping data from nofluffjobs
    * [pracuj_scraper](scrapers/pracuj_scraper.py) - class for scraping data from pracuj.pl
* [sql_app](sql_app) - package where are files related to SQLAlchemy library, and connecting database to fastapi server
    * [crud](sql_app/crud.py) - file with crud operation on 
    * [database](sql_app/database.py) - file with setting up connection do database
    * [models](sql_app/models.py) - file with classes which interact with database
    * [schemas](sql_app/schemas.py) - file with Pydantic models which are valid data shape, this class are return to user from database
    * [website_names](sql_app/website_names.py) - file with enum class of all pages from which data are scraped 

### Server API

| Resource | Description |
|:---------|:------------|
|`/`       |Always return "Hello world"|
|`offers/{website}`| Return offers for specified website|
|`offers/offer/{offer_id}`| Return offer of specified id if exist|
|`offers/`|Return all offers|

All offers resources will give first 100 offers. 
To get next or less you must use query parameters. Ex:

https://job-offers-scraper.herokuapp.com/offers?skip=10&limit=10 will give you second tenth of offers on page.

