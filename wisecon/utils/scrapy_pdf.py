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

    def __init__(self, target_url=None, result_obj=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.target_url = target_url
        self.result_obj = result_obj

    def start_requests(self):
        if self.target_url:
            yield Request(url=self.target_url, callback=self.parse_pdf)
        else:
            self.logger.error("未提供 target_url")

    def parse_pdf(self, response):
        if self.result_obj:
            self.result_obj.bytes_data = response.body


def fetch_pdf_bytes(url: str) -> bytes:
    """"""
    pdf_response = PDFResponse()
    process = CrawlerProcess({'LOG_LEVEL': 'WARNING'})
    process.crawl(PDFSpider, target_url=url, result_obj=pdf_response)
    process.start()
    return pdf_response.bytes_data
