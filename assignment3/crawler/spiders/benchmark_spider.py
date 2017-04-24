import re, scrapy
from crawler.items import *

class BenchmarkSpider(scrapy.Spider):
    drop_params = True
    # Spider name, for use with the scrapy crawl command
    name = "benchmarks"

    # Constants to get url parts
    FULL, PROTOCOL, USER, PASSWORD, SUBDOMAIN, DOMAIN, TOP_LEVEL_DOMAIN, PORT_NUM, PATH, PAGE, GET_PARAMS, HASHTAGS = range(12)

    # List of start urls to start crawling
    start_urls = [
        # 'https://app1.com',
        # 'https://app2.com',
        # 'https://app3.com',
        # 'https://app4.com',
        # 'https://app5.com',
        # 'https://app6.com',
        # 'https://app7.com',
        # 'https://app8.com',
        # 'https://app9.com',
        # 'https://app10.com',
        # 'https://app11.com',
        'http://ec2-54-255-215-139.ap-southeast-1.compute.amazonaws.com/'
    ]
    allowed_domains = [
        "app1.com", 
        "app2.com",
        "app3.com", 
        "app4.com", 
        "app5.com", 
        "app6.com", 
        "app7.com", 
        "app8.com", 
        "app9.com", 
        "app10.com", 
        "app11.com",
        "app12.com",
        "app13.com",
        "app14.com",
        "app15.com",
        "app16.com",
        "app17.com",
        "app18.com",
        "app19.com",
        "app20.com",
        "app21.com"
    ]

    # Set to keep track of visited urls
    visited_urls = set(start_urls)

    """ 
    Uses Regex to split up url into components. Groups and what they are:
        0 : the full url
        1 : Protocol
        2 : User
        3 : Password
        4 : Subdomain
        5 : Domain
        6 : Top level domain (.com .net etc)
        7 : Port number
        8 : Path
        9 : Page
        10: Get parameters
        11: Hashtags 
    """
    def splitUrlIntoParts(self, url, index):
        pattern = '(?:([^\:]*)\:\/\/)?(?:([^\:\@]*)(?:\:([^\@]*))?\@)?(?:([^\/\:]*)\.(?=[^\.\/\:]*\.[^\.\/\:]*))?([^\.\/\:]*)(?:\.([^\/\.\:#]*))?(?:\:([0-9]*))?(\/[^\?#]*(?=.*?\/)\/)?([^\?#]*)?(?:\?([^#]*))?(?:#(.*))?'
        match = re.search(pattern, url)
        if match:
            if match.group(index):
                return match.group(index)
        return ''

    def populateURLItem(self, item, url):
        item['url'] = url

        item['protocol'] = self.splitUrlIntoParts(url, self.PROTOCOL)
        item['domain'] = self.splitUrlIntoParts(url, self.DOMAIN)
        item['path'] = self.splitUrlIntoParts(url, self.PATH)
        item['page'] = self.splitUrlIntoParts(url, self.PAGE)
        item['get_params'] = self.splitUrlIntoParts(url, self.GET_PARAMS)

    def getUrlWithoutParams(self, url):
        # Pattern looks out for a question mark that marks start of params
        # Assumption is that url is already valid
        pattern = '([^? ]+).*'

        match = re.search(pattern, url)

        if match:
            if match.group(1):
                return match.group(1)
            else:
                return ''

    def isVisited(self, url):
        if self.drop_params:
            truncated_url = self.getUrlWithoutParams(url)
            return truncated_url in self.visited_urls
        else :
            return url in self.visited_urls

    def markAsVisited(self, url):
        if self.drop_params:
            truncated_url = self.getUrlWithoutParams(url)
            self.visited_urls.add(truncated_url)
        else:
            self.visited_urls.add(url)


    # The default method that's called by scrapy for each url in the start_url list
    def parse(self, response):
        # Get URL item
        item = URLItem()
        # Get parts of URL item
        self.populateURLItem(item, response.url)
        yield item

        # Look for Forms
        # Assumption: forms will have id attribute
        # We will be using this id and url to uniquely identify each form
        forms = response.css('form')
        for form in forms:
            formItem = FormItem()
            formItem['url'] = response.url
            form_id = form.css('::attr(id)').extract_first()
            if form_id is None:
                form_id = ''
            formItem['id_attr'] = form_id
            yield formItem
            inputs = form.css('input')
            for a in inputs:
                inputItem = InputItem()
                inputItem['url'] = response.url
                inputItem['form_id'] = form_id
                inputItem['complete'] = a.extract()
                inputItem['type_attr'] = a.css('::attr(type)').extract_first()
                yield inputItem

        # Get url to visit next
        links = response.css('a::attr(href)').extract()
        for next_page in links:
            # Check that url exist
            if next_page is not None:
                # Handle weirdass cases where hrefs has scheme:///domain
                next_page = next_page.replace("///", "//", 1)
                next_page = response.urljoin(next_page)
                # Check that url is not visited yet
                if not self.isVisited(next_page):
                    self.markAsVisited(next_page)
                    yield scrapy.Request(next_page, callback=self.parse)