from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
import requests
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    #latest news Mars scrape
    url_latest_news = 'https://mars.nasa.gov/news/'
    browser.visit(url_latest_news)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    result = soup.find('div', class_='list_text')
    news_title = result.a.text
    news_p = result.find('div', class_='article_teaser_body').text

    #scrape Mars facts
    url_image = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(url_image)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    src = soup.footer.a['data-fancybox-href']
    featured_img_url = f'https://www.jpl.nasa.gov{src}'

    #High resoltution images for each hemisphere
    url_hem = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(url_hem)
    time.sleep(1)
    html = browser.html
    soup = bs(html, 'html.parser')
    items = soup.find_all('div', class_='item')
    hemisphere_image_urls=[]
    for item in items:
        href = item.a['href']
        url_hem_ref = f'https://astrogeology.usgs.gov/{href}'
        browser.visit(url_hem_ref)
        html = browser.html
        soup = bs(html,'html.parser')
        time.sleep(1)
        hem_url = soup.find('div',class_='downloads').\
            find('a')['href']
        title = soup.find('div', class_='content').\
            find('h2',class_='title').text 
        dict={}
        dict['title']=title
        dict['img_url']= hem_url
        hemisphere_image_urls.append(dict)
    browser.quit()

    #Mars facts
    url_facts = 'https://space-facts.com/mars/'
    tables = pd.read_html(url_facts)
    mars_df = tables[0]
    mars_df.rename({0:'Infos', 1:'Unit'}, axis=1, inplace=True)
    mars_df['Infos'] = mars_df['Infos'].str.replace(':','')
    mars_table = mars_df.to_dict('records')
    f = open('data/mars_table.html','w', encoding='utf-8')
    mars_df.to_html(buf = f, index=False)
    f.close()

    #store all the data in a dictionnary
    mars_data={
        'news_title' : news_title,
        'news_p' : news_p,
        'mars_table' : mars_table,
        'featured_img_url': featured_img_url,
        'hemisphere_image_urls' : hemisphere_image_urls
        }

    # Return results
    return mars_data