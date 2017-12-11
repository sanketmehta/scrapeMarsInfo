from bs4 import BeautifulSoup

import pandas as pd
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver

from datetime import datetime


def scrape():
    dt = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
    print(dt)

    # Start the WebDriver and load the page
    wd = webdriver.Chrome()
    wd.get('https://mars.nasa.gov/news/')

    # Wait for the dynamically loaded elements to show up
    WebDriverWait(wd, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "content_title")))

    # And grab the page HTML source
    html_page = wd.page_source
    wd.quit()

    # Now you can use html_page as you like
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_page, "lxml")

    news_title = soup.find('div', {'class': 'content_title'}).getText()

    news_p = soup.find('div', {'class': 'article_teaser_body'}).getText()

    nasa_website_base = "https://www.jpl.nasa.gov"

    # Start the WebDriver and load the page
    wd = webdriver.Chrome()
    wd.get('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # Wait for the dynamically loaded elements to show up
    WebDriverWait(wd, 20).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "carousel_items")))

    # And grab the page HTML source
    html_page = wd.page_source
    wd.quit()

    soup1 = BeautifulSoup(html_page, "lxml")


    for aa1 in soup1.find_all('article'):
        style1 = aa1.get('style', {'background-image': 'url'})
        image_href = style1.split("'")[1]

    featured_image_url = nasa_website_base + image_href
    print(featured_image_url)

    r2 = requests.get("https://twitter.com/marswxreport?lang=en")
    data2 = r2.text
    soup2 = BeautifulSoup(data2, "lxml")

    first_div = soup2.find('div')
    para1 = first_div.find('p', {"class": "TweetTextSize"}).getText()

    mars_weather = para1
    print(mars_weather)

    r3 = requests.get("https://space-facts.com/mars/")
    data3 = r3.text
    soup3 = BeautifulSoup(data3, "lxml")

    mars_table = soup3.find('table', {"class": "tablepress-id-mars"})
    attr1, val1 = [], []
    for row in mars_table.findAll('tr'):
        for col in row.findAll('td', {"class": "column-1"}):
            attr1.append(col.getText())
        for col in row.findAll('td', {"class": "column-2"}):
            val1.append(col.getText())

    df_mars = pd.DataFrame({'description':attr1,
                        'value':val1})

    df_mars.set_index('description', inplace=True)
    print(df_mars)


    astrogeology_base = "https://astrogeology.usgs.gov/"
    r4 = requests.get("https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars")
    data4 = r4.text
    soup4 = BeautifulSoup(data4, "lxml")


    hemisphere_image_urls = []
    for x in soup4.findAll('a', {'class':'item product-item'}):

        url6 = astrogeology_base + x.get('href')
        r6 = requests.get(url6)
        data6 = r6.text
        soup6 = BeautifulSoup(data6, "lxml")
        
        for x6 in soup6.findAll('img', {'class':'wide-image'}):
            hemisphere_image_urls.append({'title':x.h3.text,
                                    'img_url':astrogeology_base + x6.get('src')})


    hemisphere_image_urls

    mongo_df = {'time': dt,
                'news_title': news_title,
                'news_p': news_p,
                'featured_image_url': featured_image_url,
                'mars_weather': mars_weather,
                'df_mars': df_mars.to_json(),
                'hemisphere_image_urls': hemisphere_image_urls}

    return(mongo_df)


