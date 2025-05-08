import multiprocessing
from typing import Dict
from scrapy import Spider, Request
from scrapy.crawler import CrawlerProcess


__all__ = [
    "PDFSpider",
    "PDFResponse",
    "fetch_pdf_bytes",
]


class PDFResponse:
    def __init__(self):
        self.bytes_data = None


class PDFSpider(Spider):
    name = 'pdf_spider'

    def __init__(self, target_url=None, result_obj=None, headers=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_url = target_url
        self.result_obj = result_obj
        self.headers = headers

    def start_requests(self):
        if self.target_url:
            yield Request(url=self.target_url, callback=self.parse_pdf, headers=self.headers)
        else:
            self.logger.error("未提供 target_url")

    def parse_pdf(self, response):
        if self.result_obj:
            self.result_obj.bytes_data = response.body


def pdf_spider_worker(url, headers, return_dict):
    """子进程执行函数"""
    result_obj = PDFResponse()
    process = CrawlerProcess({
        'LOG_LEVEL': 'WARNING',
        'LOG_FORMATTER': 'scrapy.logformatter.LogFormatter',
    })
    process.crawl(PDFSpider, target_url=url, result_obj=result_obj, headers=headers)
    process.start()
    return_dict['bytes'] = result_obj.bytes_data


def fetch_pdf_bytes(url: str, headers: Dict) -> bytes:
    """"""
    manager = multiprocessing.Manager()
    return_dict = manager.dict()
    p = multiprocessing.Process(target=pdf_spider_worker, args=(url, headers, return_dict))
    p.start()
    p.join()
    return return_dict.get('bytes')
