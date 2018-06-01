# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import tweepy
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pandas as pd

# Chrome Driver
executable_path = {'executable_path': 'C:/Users/Sonia/Documents/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)

# MARS NEW
def marsNews():
    # URL of page to be scraped
    news_url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"

    # visit the page and retrieve the html and parse
    browser.visit(news_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # store the latest title in a variable
    news_title = soup.find('div', class_='content_title').text
    print(news_title)

    # store the latest paragraph
    news_p = soup.find('div', class_='article_teaser_body').text
    print(news_p)
    
    news_info = [news_title, news_p]
    return news_info


# MARS SPACE IMAGES - FEATURED IMAGES
def marsFeaturedImage():
    # URL of page to be scraped
    mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    # visit the page and retrieve the html and parse
    browser.visit(mars_images_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    featured_image = soup.find('article', class_='carousel_item')['style']

    # extract the URL from the string by splitting using ' as a delimiter
    featured_image_split = featured_image.split("'")
    
    # extract the desired needed URL portion and append it to the main JPL site 
    # a bit hacky and hardcoded, but gets the job done without resorting to loading dynamic elements
    # still a viable solution since the inline CSS formatting will not change among rotating featured images

    featured_image_url = "https://www.jpl.nasa.gov" + featured_image_split[1]
    print(featured_image_url)
    return featured_image_url


# MARS WEATHER
def marsWeather():
    # Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 

    # Setup Tweepy API Authentication
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
    
    # Retrieve and store the latest tweet
    target_user = "MarsWxReport"
    tweet = api.user_timeline(target_user, count = 1)
    mars_weather = (tweet[0]['text'])
    print(mars_weather)
    return mars_weather

# MARS FACTS
def marsFacts():
    # Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
    # Use Pandas to convert the data to a HTML table string.

    mars_facts_url = "http://space-facts.com/mars/"

    tables = pd.read_html(mars_facts_url)
    print(tables)
    return tables


# MARS HEMISPHERES
def marsHemispheres():
    # Visit the USGS Astrogeology site here to obtain high resolution images for each of Mar's hemispheres.

    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    # this gets the whole element not just the href
    hemispheres = soup.find_all('a', class_='itemLink product-item')

    # make a list to store the hrefs
    hemisphere_hrefs = []

    for hemisphere in hemispheres:
        hemisphere_hrefs.append(hemisphere['href'])


    # function to extract unique values since we have duplicates
    def unique(my_list):
     
        # intilize a null list
        unique_list = []
         
        # traverse for all elements
        for x in my_list:
            # check if exists in unique_list or not
            if x not in unique_list:
                unique_list.append(x)
            
        return unique_list
            
    hemisphere_list = unique(hemisphere_hrefs)

    hemisphere_image_urls = []

    for href in hemisphere_list:
        # visit each link and then pull the full image link from each page
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        image_link = "https://astrogeology.usgs.gov" + href

        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})
        
    print(hemisphere_image_urls)
    return hemisphere_image_urls


# SCRAPE FUNCTION TO CALL EVERYTHING ELSE 
def scrape():
    mars_data = {}
    
    mars_data["mars_news"] = marsNews()
    mars_data["mars_image"] = marsFeaturedImage()
    mars_data["mars_weather"] = marsWeather()
    mars_data["mars_facts"] = marsFacts()
    mars_data["mars_hemisphere"] = marsHemispheres()
    
    return mars_data
    
#testing purposes only
#scrape();