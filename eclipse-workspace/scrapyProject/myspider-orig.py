import django
import logging
import sys
from tkinter import *

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.http.request import Request
from twisted.application.reactors import Reactor

print("The location of Scrapy is:")
print (scrapy.__file__)


# S C R A P Y    S T U F F
#
logging.getLogger('myScrapy').setLevel(logging.WARNING)
runner = CrawlerRunner({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
 

# Tk stuff: Python native GUI

 
def callback_quit():
    print("quit button pressed")
    sys.exit()

root = Tk()
root.wm_title("Scrapy Demo")


def callback_scrape():
    theUrl = chosenUrl.get()
    print("theUrl:"+theUrl)
    chosenUrl.set(theUrl)
    
    deferredCallback = runner.crawl(ScrapeSpider)
    deferredCallback.addBoth(lambda _: reactor.stop())  #@UndefinedVariable
    reactor.run() #@UndefinedVariable



#b2 = Button(root, text="Scrape Quotes", command=callback_quotes)
#b2.pack()
urls = ("Choose URL to Scrape",
    "http://speechkitchen.org/category/whats-cooking",
    "http://quotes.toscrape.com/tag/humor/")

chosenUrl = StringVar(root)
chosenUrl.set(urls[1])
e = OptionMenu(root, chosenUrl, *urls)


e.grid(row=0,column=0)


b3 = Button(root, text="Quit", command=callback_quit)
b3.grid(row=0,column=1)

lab = Label(root, textvariable=chosenUrl)
lab.grid(row=1)

b = Button(root, text="Scrape", command=callback_scrape)
b.grid(row=2,column=1)

entrytitle_var=IntVar()
divquote_var=IntVar()

entrytitle = Checkbutton(root, text='h1.entry-title', variable=entrytitle_var)
divquote = Checkbutton(root, text='div.quote', variable=divquote_var)

entrytitle.grid(row=3,column=0)
divquote.grid(row=4,column=0)

tex = Text()
tex.grid(row=5,column=0,columnspan=2,sticky=W+E+N+S)

Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)

class ScrapeSpider(scrapy.Spider):
    name = 'scrapespider'

    start_urls = [''] # fill in later
    
    # fills in start_urls
    def start_requests(self):
        theUrl = chosenUrl.get()
        print("spider Url: "+theUrl)
        yield Request(theUrl, self.parse)
 
    def parse(self, response):
        # Pulls out text part of all the <h1 class="entry-title"> elements like:
        #
        # <h1 class="entry-title">
        #  <a href="http://speechkitchen.org/eesen-offline-transcriber/" rel="bookmark">
        #  EESEN offline transcriber</a>
        #  <a ...>
        #  foofoofoo</a>
        #  ...
        # </h1>
        #
        for title in response.css('h1.entry-title'):
            #print (title.css('a::text').extract_first())
            tex.insert(END, "css  :'a::text' " +
                       title.xpath('a/text()').extract_first() + "\n\n")
            tex.see(END)
            yield {'title': title.css('a::text').extract_first()}
            
#         for entry in response.css('div.entry-content'):
#             #print (quote.css('span.text::text').extract_first())
#             #print (quote.xpath('span/small/text()').extract_first())
#             tex.insert(END, "xpath:'p/text()' " +
#                        entry.xpath('p/text()').extract_first() + "\n\n")
#             tex.see(END)
#             
#             yield {
#                 'text': entry.css('span.text::text').extract_first(),
#                 'author': entry.xpath('span/small/text()').extract_first(),
#                 }

        print("before")
        for art in response.css('article'):
            print(art.xpath('.//h1/*/text()').extract())
            
            #print ("title:"+art.xpath('header/h1/text()').extract())
            #print ("content:"+art.xpath('.//div/p/text()').extract())
        print("after")
            
 
        # pulls out text and title part of all the <div class="quote"> elements like:
        #
        # <div class="quote"> itemscope="" itemtype="http://schema.org/CreativeWork">
        # <span class="text" itemprop="text>
        #   "The person bla bla bla, quotey quote quote"
        # </span>
        # ...
        # </div>
        for quote in response.css('div.quote'):
            #print (quote.css('span.text::text').extract_first())
            #print (quote.xpath('span/small/text()').extract_first())
            tex.insert(END, "css  :'span.text::text' "  +
                       quote.css('span.text::text').extract_first() + "\n")
            tex.insert(END, "xpath:'span/small/text()' " +
                       quote.xpath('span/small/text()').extract_first() + "\n\n")
            tex.see(END)
            
            yield {
                'text': quote.css('span.text::text').extract_first(),
                'author': quote.xpath('span/small/text()').extract_first(),
                }
 
        #next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
        #if next_page:
        #    yield myScrapy.Request(response.urljoin(next_page), callback=self.parse)
 
# class QuotesSpider(scrapy.Spider):
#     name = "quotes"
#     start_urls = [
#         'http://quotes.toscrape.com/tag/humor/',
#         ]
#  
#     def parse(self, response):
#         for quote in response.css('div.quote'):
#             print (quote.css('span.text::text').extract_first())
#             print (quote.xpath('span/small/text()').extract_first())
#             yield {
#                 'text': quote.css('span.text::text').extract_first(),
#                 'author': quote.xpath('span/small/text()').extract_first(),
#                 }
#  
#             next_page = response.css('li.next a::attr("href")').extract_first()
#             if next_page is not None:
#                 next_page = response.urljoin(next_page)
#                 yield scrapy.Request(next_page, callback=self.parse)
 

 

 

mainloop()
#root.mainloop()
