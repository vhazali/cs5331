import re
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from crawler.items import *

class QuotesSpider(scrapy.Spider):
    # Spider name, for use with the scrapy crawl command
    name = "quotes"
    # List of start urls to start crawling
    start_urls = [
        'https://ivle.nus.edu.sg',
    ]
    allowed_domains = ["ivle.nus.edu.sg"]

    # Set to keep track of visited urls
    visited_urls = set(start_urls)

    # Function to get protocol of url
    def getProtocol(self, url):
        pattern = '^[^:]+(?=:\/\/)'
        protocol = re.search(pattern, url)
        if protocol:
            return protocol.group(0)
        else:
            return ''

    # The default method that's called by scrapy for each url in the start_url list
    def parse(self, response):
        urlItem = URLItem()
        urlItem['url'] = response.url
        urlItem['protocol'] = self.getProtocol(response.url)
        print(urlItem)
        
        # Find login forms
        inputList = list()
        forms = response.css('form')
        for form in forms:
            formItem = FormItem()
            formItem['url'] = response.url
            form_id = form.css('::attr(id)').extract_first()
            formItem['id_attr'] = form_id
            print (formItem)
            inputs = form.css('input')
            for a in inputs:
                inputItem = InputItem()
                inputItem['form_id'] = form_id
                inputItem['complete'] = a.extract()
                inputItem['type_attr'] = a.css('::attr(type)').extract()
                print(inputItem)

        # Get url to visit next
        # links = response.css('a::attr(href)').extract()
        # for next_page in links:
        #     # Check that url exist
        #     if next_page is not None:
        #         next_page = response.urljoin(next_page)
        #         # Check that url is not visited yet
        #         if next_page not in self.visited_urls:
        #             self.visited_urls.add(next_page)
        #             yield scrapy.Request(next_page, callback=self.parse)


# class RunCrawler():
    
#     def start_crawl(self):
#         process = CrawlerProcess(get_project_settings())
#         process.crawl(QuotesSpider)
#         process.start()