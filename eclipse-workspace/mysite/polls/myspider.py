import logging
import myScrapy
from scrapy.crawler import CrawlerProcess
from Tkinter import *
import django

print(django.get_version())
sys.exit()

logging.getLogger('myScrapy').setLevel(logging.WARNING)

class BlogSpider(myScrapy.Spider):
    name = 'blogspider'
    start_urls = ['http://speechkitchen.org/category/whats-cooking',
                  'http://quotes.toscrape.com/tag/humor/']

    def parse(self, response):
        for title in response.css('h1.entry-title'):
            print title.css('a ::text').extract_first()
            yield {'title': title.css('a ::text').extract_first()}

        for quote in response.css('div.quote'):
            print quote.css('span.text::text').extract_first()
            print quote.xpath('span/small/text()').extract_first()
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
                }

        #next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
        #    yield myScrapy.Request(response.urljoin(next_page), callback=self.parse)

class QuotesSpider(myScrapy.Spider):
    name = "quotes"
    start_urls = [
        'http://quotes.toscrape.com/tag/humor/',
        ]

    def parse(self, response):
        for quote in response.css('div.quote'):
            print quote.css('span.text::text').extract_first()
            print quote.xpath('span/small/text()').extract_first()
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
                }

            next_page = response.css('li.next a::attr("href")').extract_first()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield myScrapy.Request(next_page, callback=self.parse)

process = CrawlerProcess({
#    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

# Tk stuff: Python native GUI
def callback_blog():
    process.crawl(BlogSpider)
    process.start()

def callback_quotes():
    process.crawl(QuotesSpider)
    process.start()

def callback_quit():
    sys.exit()

logging.getLogger('myScrapy').setLevel(logging.WARNING)

root = Tk()
root.wm_title("Scrapy Demo")
b = Button(root, text="Scrape What's Cooking", command=callback_blog)
b.pack()
b2 = Button(root, text="Scrape Quotes", command=callback_quotes)
b2.pack()
b3 = Button(root, text="Quit", command=callback_quit)
b3.pack()
mainloop()
#root.mainloop()
