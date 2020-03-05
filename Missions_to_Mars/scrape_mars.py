# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd

def init_browser():
   executable_path = {"executable_path":r"C:/bin/chromedriver"}
   return Browser('chrome', **executable_path, headless=False) 

def scrape():
   browser = init_browser()

   # Visit the mars Nasa news site
   url = 'https://mars.nasa.gov/news/'
   browser.visit(url)

   # Scrape page into soup
   browser_html = browser.html
   news_soup = bs(browser_html, "html.parser")

   # Get most recent headline
   slide_element = news_soup.select_one("ul.item_list li.slide")
   news_title = slide_element.find("div", class_="content_title").find("a").text

   # Get first snippet of article text
   news_p = slide_element.find("div", class_="article_teaser_body").text

   # Store data in a dictionary
   news_data = {
      "Top News": news_title,
      "Teaser": news_p
   }

   # Close the browser after scraping
   browser.quit()

   return news_data
