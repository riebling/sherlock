
import logging
import sys
from tkinter import *

# Tk stuff: Python native GUI
def callback_blog():
    print ('callback_blog called')

 
def callback_quotes():
    print ('callback_quotes called')

 
def callback_quit():
    sys.exit()
     
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
