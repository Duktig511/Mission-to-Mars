import pymongo
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import os


def init_browser():
    #Replace the path with your actual path to the chromedriver
    exe_path = os.path.join('C:\Program Files (x86)\Google\Chrome\Application', 'chromedriver')
    executable_path = {'executable_path': exe_path}
    return Browser("chrome", **executable_path, headless=False)


def scrape(update_db=False, update_scrape='All'):

    #instantiate browser and dictionary for output
    browser = init_browser()
    mars_info = {}

    #Translate function input args to a specified call function call within 'Update' dictionary
    update_call = update_scrape
    func_call = f'Update {update_call}'

    #Dictionary storing all scrape functions as strings to suspend execution
    Update_dict = {'Update All':['mars_info.update(scrape_mars_news(browser))',
    'mars_info.update(scrape_mars_image(browser))',
    'mars_info.update(scrape_mars_weather(browser))',
    'mars_info.update(scrape_mars_facts(browser))',
    'mars_info.update(scrape_mars_hemispheres(browser))'],
    'Update News':'mars_info.update(scrape_mars_news(browser))',
    'Update Image':'mars_info.update(scrape_mars_image(browser))',
    'Update Weather':'mars_info.update(scrape_mars_weather(browser))',
    'Update Facts':'mars_info.update(scrape_mars_facts(browser))',
    'Update Hemispheres':'mars_info.update(scrape_mars_hemispheres(browser))'}

    #Iterate through specified fuction call and check for nested items then apply eval() method to activate function references 
    for key, value in Update_dict.items():
        if key == func_call:
            if type(value)!=list:
                eval(value)
            else:
                for count, item in enumerate(value):
                    eval(value[count])

    browser.quit()

    if update_db==True:
        UpdateMongo(mars_info)

    return mars_info

def scrape_mars_news(brwsr):
    
    browser = brwsr
    mars_news = {}
    # Visit Nasa news url through splinter module
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    proceed = browser.is_text_present('article_teaser_body', wait_time=5)

    # HTML Object
    if proceed==True:
        html = browser.html
    else:
        proceed = browser.is_text_present('article_teaser_body', wait_time=8)
        html = browser.html
    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html, 'html.parser')


    # Retrieve the latest element that contains news title and news_paragraph
    news_title = soup.find('div', class_='content_title').find('a').text
    news_p = soup.find('div', class_='article_teaser_body').text

    # Dictionary entry from MARS NEWS
    mars_news['news_title'] = news_title
    mars_news['news_paragraph'] = news_p

    return mars_news



def scrape_mars_image(brwsr):

    browser = brwsr
    mars_image = {}
    # Visit Mars Space Images through splinter module
    image_url_featured = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(image_url_featured)# Visit Mars Space Images through splinter module

    # HTML Object 
    html_image = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_image, 'html.parser')

    # Retrieve background-image url from style tag 
    featured_image_url  = soup.find('article')['style'].replace('background-image: url(','').replace(');', '')[1:-1]

    # Website Url 
    main_url = 'https://www.jpl.nasa.gov'

    # Concatenate website url with scrapped route
    featured_image_url = main_url + featured_image_url

    # Display full link to featured image
    featured_image_url 

    # Dictionary entry from FEATURED IMAGE
    mars_image['featured_image_url'] = featured_image_url 
    
    return mars_image



def scrape_mars_weather(brwsr):

    browser = brwsr
    mars_weather = {}
    # Visit Mars Weather Twitter through splinter module
    weather_url = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather_url)

    # HTML Object 
    html_weather = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_weather, 'html.parser')

    # Find all elements that contain tweets
    new_twts = soup.find_all('div', class_='js-tweet-text-container')

    # Retrieve all elements that contain news title in the specified range
    # Look for entries that display weather related words to exclude non weather related tweets 
    for twt in new_twts: 
        weather_twt = twt.find('p').text
        if 'Sol' and 'pressure' in weather_twt:
            print(weather_twt)
            break
        else: 
            pass

    # Dictionary entry from WEATHER TWEET
    mars_weather['weather_twt'] = weather_twt
    
    return mars_weather


def scrape_mars_facts(brwsr):

    browser = brwsr
    marsFacts = {}
    # Visit Mars facts url 
    facts_url = 'http://space-facts.com/mars/'

    # Use Panda's `read_html` to parse the url
    mars_facts = pd.read_html(facts_url)

    # Find the mars facts DataFrame in the list of DataFrames as assign it to `mars_df`
    mars_df = mars_facts[0]

    # Assign the columns `['Description', 'Value']`
    mars_df.columns = ['Description','Value']

    # Set the index to the `Description` column without row indexing
    mars_df.set_index('Description', inplace=True)

    # Save html code to folder Assets
    data = mars_df.to_html()

    # Dictionary entry from MARS FACTS
    marsFacts['mars_facts'] = data

    return marsFacts


def scrape_mars_hemispheres(brwsr):

    browser = brwsr
    mars_hemispheres = {}
    # Visit hemispheres website through splinter module 
    hemispheres_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemispheres_url)

    # HTML Object
    html_hemispheres = browser.html

    # Parse HTML with Beautiful Soup
    soup = BeautifulSoup(html_hemispheres, 'html.parser')

    # Retreive all items that contain mars hemispheres information
    items = soup.find_all('div', class_='item')

    # Create empty list for hemisphere urls 
    h_list = []

    # Store the main_ul 
    hemispheres_main_url = 'https://astrogeology.usgs.gov' 

    # Loop through the items previously stored
    for i in items: 
        # Store title
        title = i.find('h3').text
        
        # Store link that leads to full image website
        partial_img_url = i.find('a', class_='itemLink product-item')['href']
        
        # Visit the link that contains the full image website 
        browser.visit(hemispheres_main_url + partial_img_url)
        
        # HTML Object of individual hemisphere information website 
        partial_img_html = browser.html
        
        # Parse HTML with Beautiful Soup for every individual hemisphere information website 
        soup = BeautifulSoup( partial_img_html, 'html.parser')
        
        # Retrieve full image source 
        img_url = hemispheres_main_url + soup.find('img', class_='wide-image')['src']
        
        # Append the retreived information into a list of dictionaries 
        h_list.append({"title" : title, "img_url" : img_url})

    mars_hemispheres['h_list'] = h_list

    
    # Return mars_data dictionary 

    return mars_hemispheres


def UpdateMongo(scrape_values):

    # Setup connection to mongodb
    conn = "mongodb://localhost:27017/Mars_App"
    client = pymongo.MongoClient(conn)
    # Select database and collection to use
    db = client.Mars_App

    # Create Team collection
    collection = db.Mars_Data

    # If we want to drop the data upon every execution, re-add the line below.
    collection.drop()

    # Creates a collection in the database and inserts two documents
    for key, value in scrape_values.items():
        collection.insert_one({key:value})



mars_dict = scrape(update_db=True, update_scrape='All')
print(mars_dict)