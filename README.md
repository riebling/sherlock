# sherlock
working area for documents related to sherlock demo

Timeline activities
 - familiarize with Scrapy (as stated previously)
 - prototype some simple scraping use case (the Scrapy 'hello world' example)
 - fill out this document, breaking down system components, describing data, use cases

Decision: we will use Vagrant to provision and run sherlock demo in (and make easily shareable) a virtual machine
   
Stream-of-consciousness Questions:
0. Configuration: how to configure e.g. Scrapy
 - how much knowledge of web structure is required of analysts ('end-users') vs. developers (us): it's clear some,
1.  for example the demo knows about CSS tags:
  ```for title in response.css('h2.entry-title'):```
  as it turns out, to try the demo on a different site (speechkitchen.org) the CSS for title-to-be-scraped needs to be changed to ```h1.entry-title```
2.  div tags:
  ```yield {'title': title.css('a ::text').extract_first()}```
so there's a bit of chicken-and-egg going on here: you have to know what you're looking for, before you look for it
3.  recursion:
  ```next_page = response.css('div.prev-post > a ::attr(href)').extract_first()```
4. output format is in JSON (nice) and includes unicode (so we need to parse JSON)
  ```{'title': u'Dirbot \u2013 a new example Scrapy project'}```
5. Selectors: specify parts of document to scrape using
 - CSS selector - if you are familiar with CSS of web pages
 - XPath (preferred, internally used by Scrapy) - more powerful e.g. "
6. Scheduling: having scrapy run asynchronously e.g. overnight

Tools:
 * [Web Archival Tool (WAT)](https://github.com/philpot/trafficop-wat.git)
 * Selenium - automate web 
 * Scrapy
  - Uses Python
  - requires several Python packages
    * lxml, an efficient XML and HTML parser
    * parsel, an HTML/XML data extraction library written on top of lxml,
    * w3lib, a multi-purpose helper for dealing with URLs and web page encodings
    * twisted, an asynchronous networking framework
    * cryptography and pyOpenSSL, to deal with various network-level security needs

  - strongly recommends [virtualenv](https://virtualenv.pypa.io/en/stable/installation/)
  add these to your .bashrc
  ```
  # Python virtualenv (why is this needed? a hack to work around python package version nightmares)                                                                                                  
export WORKON_HOME=$HOME/.virtualenvs
source /usr/local/bin/virtualenvwrapper.sh
```
then to use the virtualenv,
```
source ~/.bashrc
workon temp # creates new virtualenv "temp"
# do stuff, like install python packages
deactivate # leaves virtualenv
```
  * Something to parse JSON output from Scrapy - not needed, can output other formats
  * User Interface code
    We have stuff that can be re-used, implemented in a mixture of html, javascript, and PHP. It's not clear what tools or development environment (if any) were used to produce these, and some outside expertise will be likely. I've banged my head against the code trying to work out how it works, but it's unlike any normal/familiar programming language in terms of control flow and data structures
    
Risks:
  * Scrapers can break when website formats change – some websites change format yearly
  * Even a simple page refresh can change the HTML identifiers that web scrapers depend on
  * For every 300 to 500 sites you monitor, you’ll have to fix one broken script every day
  * The cost could grow to be high, as you scale to thousands of websites
    
Domains for the system - "pick two":
  * child exploitation / escort+massage services
    - Sources to scrape: backpage.com, cityvibe.com, eros.com, humaniplex.com, myredbook.com, and sugardaddyforme.com, eroticmp.com and theeroticreview.com
  * illegal immigration
  * human trafficking
  * news gathering
  * finance / corporate / stock tracking
  * ICE - economic fraud
  * TSA, CBP - background info
  
Where's the NLP:
  Surely there's some magic NLP processing we do to provide the value-added 'special sauce' that differentiates this from off-the-shelf tools
  * Named entity recognition
  * Regular expressions

Data types/structures: 
  * use XML to represent results of Scrapy queries
  * a list of tag types to search (site specific)
  * a list of tags to follow to do recursion (blog/newsfeed type site specific)
  * how to represent results?
  * "plugin" - can we define a set of plugin types for different info retrieval needs
  * Time stamping of data for trend detection
  * Canonicalization based on keys (name, location, but mostly phone number)

Plugins: how should we design our system to open up things at a level that makes sense? Plugin-based architectures are wonderful for people who want to develop and add their own. But there will have to be a spec of some kind. And maybe "create a SHERLOCK plugin" is not a use case we need or want to support.

Use case analysis:

What are the basic things a person using the system can/will do? We should list these - how do these sound:

  * Specify sites to scrape
  * Specify the format parameters for those sites (where to look)
  * Initiate (or automatic) gathering of data
  * Specify criteria for filtering of data
  * Perform filtering of data
  * present results
   - in a GUI
   - as data
     - through an API
     - in a file
     - in a RDBMS

