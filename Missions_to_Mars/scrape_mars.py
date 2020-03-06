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

   time.sleep(1)

   # Scrape page into soup
   browser_html = browser.html
   news_soup = bs(browser_html, "html.parser")

   # Get most recent headline
   slide_element = news_soup.select_one("ul.item_list li.slide")
   print(slide_element)
   news_title = slide_element.find("div", class_="content_title").find("a").text

   # Get first snippet of article text
   news_p = slide_element.find("div", class_="article_teaser_body").text

   # Scrape for JPL Mars Space Images
   # URL to visit through chromedriver
   url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
   browser.visit(url)

   time.sleep(1)

   browser.click_link_by_partial_text('FULL IMAGE')
   image_html = browser.html

   image_soup = bs(image_html, "html.parser")
   featured_img_rel = image_soup.select_one(".carousel_item").get("style")
   featured_img_rel = featured_img_rel.split("\'")[1]

   featured_img_url = f'https://www.jpl.nasa.gov{featured_img_rel}'

   # Mars Facts
   # Visit the Mars Facts webpage
   mars_facts_url = 'https://space-facts.com/mars/'
   
   # Use Pandas to read the tables from the webpage
   tables = pd.read_html(mars_facts_url)
   
   # Specify which table we want
   table_one_df = tables[0]

   # Rename the columns
   table_one_df.columns = ["Mars Planet Profile", "Values"]

   # Reset the index
   table_one_df.set_index("Mars Planet Profile", inplace=True)

   html_table = table_one_df.to_html()

   html_table = html_table.replace('\n', '')

   # Mars Hemispheres
   # Mars hemispheres url
   hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(hemi_url)

   time.sleep(1)

   # Convert the browser html to a soup object
   hemi_html = browser.html
   hemi_soup = bs(hemi_html, "html.parser")

   # Parent html that holds the title and link to individual hemispheres
   hemi_parent = hemi_soup.select_one("div.result-list div.item")
   
   
   
   
   
   # Store data in a dictionary
   mars_dictionary = {
      "Top_News": news_title,
      "Teaser_P": news_p,
      "Featured_Image": featured_img_url,
      "Mars_Info_Table": html_table}
   #print(news_data)  # DEBUG

   return mars_dictionary
