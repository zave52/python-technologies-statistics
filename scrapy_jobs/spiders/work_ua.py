from datetime import datetime

import scrapy
from scrapy.http import Response

from config import COMMON_TECHNOLOGIES
from scrapy_jobs.items import PythonVacancy


class WorkUaSpider(scrapy.Spider):
    name = "work_ua"
    allowed_domains = ["www.work.ua"]
    start_urls = ["https://www.work.ua/jobs-it-industry-it-python/"]

    def _parse_single_vacancy(self, response: Response) -> PythonVacancy:
        vacancy = PythonVacancy()

        vacancy["name"] = "".join(response.css("h1 *::text").getall())
        vacancy["company"] = response.css(
            "ul.list-unstyled a.inline span::text"
        ).get()
        vacancy["technologies"] = []
        vacancy["posted_date"] = datetime.strptime(
            response.css("time::attr(datetime)").get(),
            "%Y-%m-%d %H:%M:%S"
        ).date()
        vacancy["views"] = None
        vacancy["applications"] = None

        description = ' '.join(
            response.css("#job-description *::text").getall()
        ).lower()

        for technology in COMMON_TECHNOLOGIES:
            tech_variants = [t.lower() for t in technology.split("|")]
            tech_name = technology.split("|")[0]
            for tech in tech_variants:
                if tech in description:
                    if tech_name not in vacancy["technologies"]:
                        vacancy["technologies"].append(tech_name)
                    break

        return vacancy

    def parse(self, response: Response, **kwargs):
        for vacancy in response.css("div.card.card-hover"):
            vacancy_url = vacancy.css("h2 a::attr(href)").get()
            yield response.follow(
                vacancy_url,
                callback=self._parse_single_vacancy
            )

        next_page = response.css(
            "ul.pagination .add-left-default a::attr(href)"
        ).get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
