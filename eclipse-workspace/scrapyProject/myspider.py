import django
import logging
import sys
from tkinter import *

import scrapy
from twisted.internet import reactor
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from scrapy.http.request import Request

print("The location of Scrapy is:")
print (scrapy.__file__)


# S C R A P Y    S T U F F
#
logging.getLogger('myScrapy').setLevel(logging.DEBUG)
runner = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})
 

# Tk stuff: Python native GUI

 
def callback_quit():
    sys.exit()

root = Tk()
root.wm_title("Scrapy Demo")

running = False

def callback_scrape():
    global running
    theUrl = chosenUrl.get()
    print("theUrl:"+theUrl)
    chosenUrl.set(theUrl)
    
    tex.delete(1.0,END)
    
    myspider = ScrapeSpider(chosenOuter.get(), chosenXpath.get())
    runner.crawl(myspider, chosenOuter.get(), chosenXpath.get())
        
    if (not running):
        runner.start()
        running = True


urls = ("Choose URL to Scrape",
    "http://speechkitchen.org/category/whats-cooking",
    "http://quotes.toscrape.com/tag/humor/")
chosenUrl = StringVar(root)
chosenUrl.set(urls[1])
e = OptionMenu(root, chosenUrl, *urls)
e.grid(row=0,column=0)

b3 = Button(root, text="Quit", command=callback_quit)
b3.grid(row=0,column=1)

#lab = Label(root, textvariable=chosenUrl)
#lab.grid(row=1)

b = Button(root, text="Scrape", command=callback_scrape)
b.grid(row=2,column=1)

# Checkbuttons and their IntVars (used as boolean flags)

# Top level: what to iterate over in document
#entrytitle_var=IntVar()
#entrytitle = Checkbutton(root, text='h1.entry-title', variable=entrytitle_var)

#divquote_var=IntVar()
#divquote = Checkbutton(root, text='div.quote', variable=divquote_var)

#article_var=IntVar()
#article = Checkbutton(root, text='div.quote', variable=article_var)

#outers = [entrytitle_var, divquote_var, article_var]

outers = ("h1.entry-title",
    "div.quote",
    "div.entry-content",
    "article")
chosenOuter = StringVar(root)
chosenOuter.set(outers[0])
o = OptionMenu(root, chosenOuter, *outers)
o.grid(row=1,column=0)

xpaths = (".//h1/*/text()",
    "a/text()",
    "span/small/text()"
    )
chosenXpath = StringVar(root)
chosenXpath.set(xpaths[1])
i = OptionMenu(root, chosenXpath, *xpaths)
i.grid(row=2,column=0)

tex = Text()
tex.grid(row=5,column=0,columnspan=2,sticky=W+E+N+S)

# make stretchable
Grid.rowconfigure(root,0,weight=1)
Grid.columnconfigure(root,0,weight=1)

# example tuple to define a scrapable item
class Scrapable():
    url = ''
    element = ''
    outer = ''
    xpath = ''
    
    def __init__(self, url, element, outer, xpath):
        self.url = url
        self.element = element
        self.outer = outer
        self.xpath = xpath
    
myScrapable = Scrapable('http://speechkitchen.org/category/whats-cooking', 'h1.entry-title', 'div.quote', 'span/small/text()')

class ScrapeSpider(scrapy.Spider):
    name = 'scrapespider'
    outer = '' #'h1.entry-title'
    xpath = '' #'a/text()'
    start_urls = ['']
    
    def __init__(self, outer, xpath):
        self.outer = outer
        self.xpath = xpath
        print("__init__ outer = " + self.outer)
        print("__init__ xpath = " + self.xpath)
    
    def start_requests(self):
        theUrl = chosenUrl.get()
        print("spider Url  : "+theUrl)
        #outer = chosenOuter.get()
        #xpath = chosenXpath.get()
        #print("spider outer: "+outer)
        #print("spider xpath: "+xpath)
        yield Request(theUrl, self.parse)

    def parse(self, response):
        print("PARSE CALLED: "+self.outer + " " + self.xpath)
        for thing in response.css(self.outer):
            print("THING: ")
            print(thing)
            #print (title.css('a::text').extract_first())
            tex.insert(END, self.outer + ":" + self.xpath + ": " +
                      thing.xpath(self.xpath).extract_first() + "\n\n")
            tex.see(END)
            yield {'scraped': thing.xpath(self.xpath).extract_first()}
            

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
        
        # need xpath equivalent:                 
        #  'text': entry.css('span.text::text').extract_first(),

#  Example of how to iterate nested posts
#  
#             next_page = response.css('li.next a::attr("href")').extract_first()
#             if next_page is not None:
#                 next_page = response.urljoin(next_page)
#                 yield scrapy.Request(next_page, callback=self.parse)
 

mainloop()
#root.mainloop()
