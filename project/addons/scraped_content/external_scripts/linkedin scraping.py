import asyncio
import json
import logging
import random
import select
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException
from bs4 import BeautifulSoup

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def get_chrome_options():
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--disable-notifications')
    options.add_argument('--disable-popup-blocking')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging', 'enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument(
        'user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    )
    return options

def wait_and_find_elements(driver, selector, timeout=30):
    try:
        WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )
        return driver.find_elements(By.CSS_SELECTOR, selector)
    except TimeoutException:
        logging.warning(f"Timeout waiting for selector: {selector}")
        return []

async def scrape_linkedin_jobs(url):
    driver = None
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=get_chrome_options())

        driver.set_page_load_timeout(30)
        driver.implicitly_wait(10)

        logging.info(f"Opening page: {url}")
        driver.get(url)
        time.sleep(5)

        if any(x in driver.current_url for x in ['login', 'authwall']):
            raise Exception("Login required - Please log in to LinkedIn first")

        selectors = [
            'div.jobs-search-results-list',
            'ul.jobs-search__results-list',
            'div.scaffold-layout__list-container'
        ]

        jobs_found = False
        for selector in selectors:
            elements = wait_and_find_elements(driver, selector)
            if elements:
                jobs_found = True
                break

        if not jobs_found:
            raise TimeoutException("Could not find job listings")

        for i in range(3):
            driver.execute_script(f"window.scrollTo(0, {(i+1) * 500});")
            time.sleep(2)

        soup = BeautifulSoup(driver.page_source, 'lxml')

        job_cards = (
            soup.select('.job-search-card') or
            soup.select('.jobs-search-results__list-item') or
            soup.select('div.job-card-container')
        )

        if not job_cards:
            return json.dumps({
                "status": "warning",
                "message": "No jobs found",
                "jobs": []
            }, ensure_ascii=False, indent=2)

        jobs = []
        for card in job_cards:
            try:
                title = (
                    card.select_one('.job-search-card__title, .job-card-list__title')
                    or card.select_one('h3.base-search-card__title')
                )
                company = (
                    card.select_one('.job-search-card__subtitle, .job-card-container__company-name')
                    or card.select_one('h4.base-search-card__subtitle')
                )
                location = (
                    card.select_one('.job-search-card__location, .job-card-container__metadata-item')
                    or card.select_one('span.job-search-card__location')
                )
                link = card.select_one('a[href*="/jobs/view/"]')
                posted_date = card.select_one('.job-search-card__listdate')
                company_logo = (
                    card.select_one(".job-card-container__logo img[src]")
                    or card.select_one(".artdeco-entity-image[src]")
                    or card.select_one(".company-logo-link img[src]")
                    or card.select_one("img.company-logo[src]")
                )

                if all([title, company, location, link]):
                    job = {
                        "title": title.get_text(strip=True) if title else None,
                        "company": company.get_text(strip=True) if company else None,
                        "location": location.get_text(strip=True) if location else None,
                        "link": link["href"].split("?")[0] if link else None, # type: ignore
                        "posted_date": (
                            posted_date.get_text(strip=True) if posted_date else None
                        ),
                        "company_logo": (
                            company_logo.get("src", None)
                            if company_logo
                            else (
                                company_logo.get("data-delayed-url", None)
                                if company_logo
                                else None
                            )
                        ),
                    }
                    jobs.append(job)
            except Exception as e:
                logging.warning(f"Error extracting job data: {str(e)}")
                continue

        return json.dumps({
            "status": "success",
            "count": len(jobs),
            "jobs": jobs
        }, ensure_ascii=False, indent=2)

    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}")
        return json.dumps({
            "status": "error",
            "message": str(e)
        }, ensure_ascii=False)

    finally:
        if driver:
            driver.quit()


def save_to_json(data, filename="linkedin_jobs.json"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(json.loads(data), f, ensure_ascii=False, indent=2)
        logging.info(f" Saved Data in {filename}")
    except Exception as e:
        logging.error(f"Error in Saving Data {str(e)}")



if __name__ == "__main__":
    url = "https://www.linkedin.com/jobs/search?keywords=Python&location=Egypt"
    result = asyncio.run(scrape_linkedin_jobs(url))
    save_to_json(result)
    print(result)
