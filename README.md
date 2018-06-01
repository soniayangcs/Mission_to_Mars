
<h1>Mission to Mars, Part I: Scraping</h1>


```python
# Dependencies
from splinter import Browser
from bs4 import BeautifulSoup
import requests
import tweepy
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pandas as pd
```

<h2>Nasa Mars News</h2>


```python
# Scrape the NASA Mars News Site and collect the latest News Title and Paragragh Text. 
# Assign the text to variables that you can reference later.

# Ended up scraping using splinter because directly scraping does not give the desired results
# (this may be the NASA site protecting against it scraping)

# path for chromedriver
# to run this code on your own computer download the chromedriver from the url below and alter the file path as needed
# https://sites.google.com/a/chromium.org/chromedriver/home
executable_path = {'executable_path': 'C:/Users/Sonia/Documents/chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)
```


```python
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
```

    Mars Helicopter to Fly on NASA’s Next Red Planet Rover Mission
    NASA is adding a Mars helicopter to the agency’s next mission to the Red Planet, Mars 2020.
    

<h2>JPL Mars Space Images - Featured Image</h2>


```python
# Visit the url for JPL's Featured Space Image.
# Use splinter to navigate the site and find the image url for the current Featured Mars Image 

# URL of page to be scraped
mars_images_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

# visit the page and retrieve the html and parse
browser.visit(mars_images_url)
html = browser.html
soup = BeautifulSoup(html, "html.parser")

featured_image = soup.find('article', class_='carousel_item')['style']

print(featured_image)
```

    background-image: url('/spaceimages/images/wallpaper/PIA14924-1920x1200.jpg');
    


```python
# extract the URL from the string by splitting using ' as a delimiter
featured_image_split = featured_image.split("'")
print(featured_image_split)
```

    ['background-image: url(', '/spaceimages/images/wallpaper/PIA14924-1920x1200.jpg', ');']
    


```python
# extract the desired needed URL portion and append it to the main JPL site 
# a bit hacky and hardcoded, but gets the job done without resorting to loading dynamic elements
# still a viable solution since the inline CSS formatting will not change among rotating featured images

featured_image_url = "https://www.jpl.nasa.gov" + featured_image_split[1]
print(featured_image_url)
```

    https://www.jpl.nasa.gov/spaceimages/images/wallpaper/PIA14924-1920x1200.jpg
    

<h2>Mars Weather</h2>


```python
# Visit the Mars Weather twitter account here and scrape the latest Mars weather tweet from the page. 

# Setup Tweepy API Authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())
```


```python
# Retrieve and store the latest tweet
target_user = "MarsWxReport"
tweet = api.user_timeline(target_user, count = 1)
mars_weather = (tweet[0]['text'])
print(mars_weather)
```

    Sol 2047 (May 10, 2018), Sunny, high 3C/37F, low -71C/-95F, pressure at 7.33 hPa, daylight 05:22-17:20
    

<h2>Mars Facts</h2>


```python
# Visit the Mars Facts webpage here and use Pandas to scrape the table containing facts about the planet including Diameter, Mass, etc.
# Use Pandas to convert the data to a HTML table string.

mars_facts_url = "http://space-facts.com/mars/"

tables = pd.read_html(mars_facts_url)
tables
```




    [                      0                              1
     0  Equatorial Diameter:                       6,792 km
     1       Polar Diameter:                       6,752 km
     2                 Mass:  6.42 x 10^23 kg (10.7% Earth)
     3                Moons:            2 (Phobos & Deimos)
     4       Orbit Distance:       227,943,824 km (1.52 AU)
     5         Orbit Period:           687 days (1.9 years)
     6  Surface Temperature:                  -153 to 20 °C
     7         First Record:              2nd millennium BC
     8          Recorded By:           Egyptian astronomers]



<h2>Mars Hemispheres</h2>


```python
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
    print(hemisphere['href'])
    hemisphere_hrefs.append(hemisphere['href'])
```

    /search/map/Mars/Viking/cerberus_enhanced
    /search/map/Mars/Viking/cerberus_enhanced
    /search/map/Mars/Viking/schiaparelli_enhanced
    /search/map/Mars/Viking/schiaparelli_enhanced
    /search/map/Mars/Viking/syrtis_major_enhanced
    /search/map/Mars/Viking/syrtis_major_enhanced
    /search/map/Mars/Viking/valles_marineris_enhanced
    /search/map/Mars/Viking/valles_marineris_enhanced
    


```python
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
hemisphere_list
```




    ['/search/map/Mars/Viking/cerberus_enhanced',
     '/search/map/Mars/Viking/schiaparelli_enhanced',
     '/search/map/Mars/Viking/syrtis_major_enhanced',
     '/search/map/Mars/Viking/valles_marineris_enhanced']




```python
hemisphere_image_urls = []

for href in hemisphere_list:
    # visit each link and then pull the full image link from each page
    title = hemisphere.find("h3").text
    title = title.replace("Enhanced", "")
    image_link = "https://astrogeology.usgs.gov" + href
    print(image_link)
    browser.visit(image_link)
    html = browser.html
    soup=BeautifulSoup(html, "html.parser")
    downloads = soup.find("div", class_="downloads")
    image_url = downloads.find("a")["href"]
    hemisphere_image_urls.append({"title": title, "img_url": image_url})
    
hemisphere_image_urls
```

    https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced
    https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced
    




    [{'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/cerberus_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere '},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/schiaparelli_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere '},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/syrtis_major_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere '},
     {'img_url': 'http://astropedia.astrogeology.usgs.gov/download/Mars/Viking/valles_marineris_enhanced.tif/full.jpg',
      'title': 'Valles Marineris Hemisphere '}]



<h1>Mission to Mars, Part II: MongoDB & Flask Application</h1>

<ul>
    <li>Converted all of the above code into a Python file scrape_mars.py</li>
    <li>Set up a Flask app (app.py) that also calls the scrape() function in scrape_mars.py </li>
    <li>Selenium webdriver works, can launch and perform all the actions automated</li>
    <li>However there are still some bugs re: rendering the scraped information and displaying it on the HTML template</li>
</ul>
