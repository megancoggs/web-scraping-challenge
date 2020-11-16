# Dependencies
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time
import pandas as pd

def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return Browser('chrome', **executable_path, headless=False)

def scrape():
    browser = init_browser()

# -------------------------------------------
# NASA Mars News
# -------------------------------------------

    # URL of page to be scraped
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)
    time.sleep(2)

    # Create HTML object; parse with BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find title of most recent news article
    news_title = soup.find("div", class_ = "content_title").text.strip()
    news_title

    # Find description of most recent news article
    news_p = soup.find("div", class_ = "article_teaser_body").text.strip()
    news_p

# -------------------------------------------
# JPL Mars Space Images - Featured Image
# -------------------------------------------

    # URL of page to be scraped
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    time.sleep(2)

    # Create HTML object; parse with BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find url of featured image
    base_url = "https://www.jpl.nasa.gov/"
    image_url = soup.find("a", class_ = "button fancybox")["data-fancybox-href"]
    featured_image_url = base_url + image_url
    featured_image_url

# -------------------------------------------
# JPL Mars Space Images - Mars Facts
# -------------------------------------------

    # URL of page to be scraped
    url = "https://space-facts.com/mars/"

    # Find tables
    tables = pd.read_html(url)
    tables

    # Grab the first table
    mars_df = tables[0]
    mars_df.columns = ["Fact", "Value"]
    mars_df

    # Convert pandas DataFrame to html table string
    mars_html_table = mars_df.to_html()
    mars_html_table.replace("\n", "")

# -------------------------------------------
# JPL Mars Space Images - Mars Hemispheres
# -------------------------------------------

    # URL of page to be scraped
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    time.sleep(2)

    # Create HTML object; parse with BeautifulSoup
    html = browser.html
    soup = bs(html, "html.parser")

    # Find all "items"
    items = soup.find_all("div", class_ = "item")

    # Base url
    base_url = "https://astrogeology.usgs.gov/"

    # Create empty array
    hemisphere_image_urls = []

    # Loop through all items
    for item in items:
        
        # Store item title
        title = item.find("h3").text
        
        # Find and visit image site; find and store image link
        img_site = base_url + item.find("a")["href"]
        browser.visit(img_site)
        time.sleep(5)
        html = browser.html
        soup = bs(html, "html.parser")
        img_url = base_url + soup.find("img", class_ = "wide-image")["src"]
        
        # Store title and url to dictionary
        url_dict = {"title": title, "img_url": img_url}
        
        # Add dictionary to array
        hemisphere_image_urls.append(url_dict)

    hemisphere_image_urls

# -------------------------------------------
# Dictionary
# -------------------------------------------
    mars_dict = {}
    mars_dict["news_title"] = news_title
    mars_dict["news_p"] = news_p
    mars_dict["featured_image_url"] = featured_image_url
    mars_dict["mars_html_table"] = mars_html_table
    mars_dict["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()

    return mars_dict
