# Python code to use Scrapy to scrape contents of the Speech Kitchen site
# and pull out conetnts of "h1.entry-title" tags (blog titles)
# Also supports recursion of "div.prev-post" tags (we have none)

import scrapy

class BlogSpider(scrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://speechkitchen.org/category/whats-cooking']

    def parse(self, response):
	for title in response.css('h1.entry-title'):
            yield {'title': title.css('a ::text').extract_first()}

	next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
