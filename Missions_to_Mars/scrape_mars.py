# Dependencies
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import time
import pandas as pd
import requests as req

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

   #Mars Weather
   twitter_response = req.get('https://twitter.com/marswxreport?lang=en')
   twitter_soup = bs(twitter_response.text, "html.parser")
   tweet_containers = twitter_soup.find_all("div", class_='js-tweet-text-container')
   mars_weather = tweet_containers[0].text



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
   
   # Title text listed under parent element within <h3> code
   title = hemi_parent.find("h3").text

   # Full image located at a different url
   # First need image parent
   image_parent = hemi_parent.find("div", class_="description")

   # 'Tail' portion of url which will direct us to url with full-size image
   image_link_partial = image_parent.find("a")["href"]

   # Visit the url where the full-size image lives
   link = 'https://astrogeology.usgs.gov' + image_link_partial
   browser.visit(link)

   time.sleep(1)

   # Convert browser to html
   image_html = browser.html

   #Convert to a soup object
   image_soup = bs(image_html, "html.parser")

   # Parent element of the full-size image
   full_img_parent = image_soup.select_one("div.wide-image-wrapper div.downloads")
   
   # Find the full-size image url within the parent element
   img_url = full_img_parent.find("a")["href"]

   #Second try of hemispheres (function and loop work with Bill)
   # Mars hemispheres url
   hemi_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
   browser.visit(hemi_url)

   time.sleep(1)

   # Convert the browser html to a soup object
   hemi_html = browser.html
   hemi_soup = bs(hemi_html, "html.parser")

   # Parent html that holds the title and link to individual hemispheres
   hemi_parent = hemi_soup.select_one("div.result-list div.item")
   # Full image located at a different url
   # First need image parent
   image_parent = hemi_parent.find("div", class_="description")
   # 'Tail' portion of url which will direct us to url with full-size image
   image_link_partial = image_parent.find("a")["href"]

   def get_first_url(soup_div):
      title = soup_div.find("h3").text
      image_parent = soup_div.find("div", class_="description")
      image_link_partial = image_parent.find("a")["href"]
      return([title, image_link_partial])

   def get_image_url(page_url, browser):
      browser.visit(link)
      time.sleep(1)
      # Convert browser to html
      image_html = browser.html
      #Convert to a soup object
      image_soup = bs(image_html, "html.parser")
      # Parent element of the full-size image
      full_img_parent = image_soup.select_one("div.wide-image-wrapper div.downloads")
      # Find the full-size image url within the parent element
      img_url = full_img_parent.find("a")["href"]
    
      return(img_url)

      # Cells below work for getting the first image.  Now trying to figure out how to get all hemispheres using a loop
   results = hemi_soup.select("div.result-list div.item")
   titles = []
   img_partials = []
   parent_url = 'https://astrogeology.usgs.gov'
   hemisphere_image_urls = []
   links = []

   for result in results:
      [title, img_partial] = get_first_url(result)
      titles.append(title)
      img_partials.append(img_partial)
      link = 'https://astrogeology.usgs.gov' + img_partial
      img_url = get_image_url(link, browser)
      links.append(link)
      
      hemi_dict = {"title": title, "img_url": img_url}
      hemisphere_image_urls.append(hemi_dict)

   title_one = hemisphere_image_urls[0]['title']
   title_two = hemisphere_image_urls[1]['title']
   title_three = hemisphere_image_urls[2]['title']
   title_four = hemisphere_image_urls[3]['title']

   image_one = hemisphere_image_urls[0]['img_url']
   image_two = hemisphere_image_urls[1]['img_url']
   image_three = hemisphere_image_urls[2]['img_url']
   image_four = hemisphere_image_urls[3]['img_url']


   
   
   # Store data in a dictionary
   mars_dictionary = {
      "Top_News": news_title,
      "Teaser_P": news_p,
      "Featured_Image": featured_img_url,
      "Mars_Weather": mars_weather,
      "Mars_Info_Table": html_table,
      "First_Hemi_Title": title,
      "First_Hemi_Img": img_url,
      "Title_One": title_one,
      "Title_Two": title_two,
      "Title_Three": title_three,
      "Title_Four": title_four,
      "Image_One": image_one,
      "Image_Two": image_two,
      "Image_Three": image_three,
      "Image_Four": image_four}
   #print(news_data)  # DEBUG

   

   return mars_dictionary
