import time
from datetime import date
from typing import Generator

import scrapy
from scrapy.http import Response
from selenium.common import NoSuchElementException
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options

from scrapy_jobs.items import PythonVacancy
from config import COMMON_TECHNOLOGIES, UKRAINIAN_MONTHS


class DouSpider(scrapy.Spider):
    name = "dou"
    allowed_domains = ["dou.ua"]
    start_urls = ["https://jobs.dou.ua/vacancies/?category=Python"]

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64; rv:137.0) Gecko/20100101 Firefox/137.0',
    }

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        options = Options()
        options.add_argument("--headless")
        self.driver = Firefox(options=options)

    def closed(self, reason) -> None:
        self.driver.quit()

    def _parse_single_vacancy(self, response: Response) -> PythonVacancy:
        vacancy = PythonVacancy()

        vacancy["name"] = response.css("h1.g-h2::text").get()
        vacancy["company"] = response.css(".info .l-n a::text").get()
        vacancy["technologies"] = []
        vacancy["views"] = None
        vacancy["applications"] = None

        date_str = response.css(".date::text").get().strip()
        day, month, year = date_str.split()
        vacancy["posted_date"] = date(
            int(year), UKRAINIAN_MONTHS[month], int(day)
        )

        description = ' '.join(
            response.css(".vacancy-section *::text").getall()
        ).lower()

        for technology in COMMON_TECHNOLOGIES:
            tech_variants = [t.lower() for t in technology.split("/")]
            for tech in tech_variants:
                if tech in description:
                    if technology.split("|")[0] not in vacancy["technologies"]:
                        vacancy["technologies"].append(technology.split("|")[0])
                    break

        return vacancy

    def parse(
        self, response: Response, **kwargs
    ) -> Generator[scrapy.http.Request]:
        self.driver.get(response.url)

        try:
            more_button = self.driver.find_element(
                By.CSS_SELECTOR, ".more-btn a"
            )
            while more_button.is_displayed():
                more_button.click()
                time.sleep(0.5)
        except NoSuchElementException:
            pass

        page_html = self.driver.page_source
        response = response.replace(body=page_html)

        for vacancy in response.css("li.l-vacancy"):
            vacancy_url = vacancy.css(".title .vt::attr(href)").get()
            yield response.follow(
                vacancy_url,
                callback=self._parse_single_vacancy
            )
