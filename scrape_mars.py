# Dependencies
from os import getcwd
from os.path import join
from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from flask_pymongo import PyMongo
import pandas
from flask import Flask, render_template, jsonify, redirect
from flask_pymongo import PyMongo
import scrape_mars

conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.mars_db
collection = db.items

# app = Flask(__name__)
# mongo = PyMongo(app)

def init_browser():
    executable_path = {'executable_path': 'chromedriver'}
    browser = Browser('chrome', **executable_path, headless=False)

url = "https://mars.nasa.gov/news/"
browser.visit(url)

# @app.route("/scrape")

def scrape():
    scrape_dict={}
# Retrieve page with the requests module
# Create BeautifulSoup object; parse with 'lxml'
    Nasa_html = browser.html
    soup=bs(Nasa_html, 'html.parser')
    # Retrieve the parent divs for all articles
    # results = soup.find('div',class_='list_text')
    news_title = soup.find_all('div',class_='content_title')
    news_paras = soup.find_all('div',class_='rollover_description_inner')
    latest_title=news_title[0].text
    latest_para=news_paras[0].text
    scrape_dict["latest_title"]=latest_title
    scrape_dict["latest_para"]=latest_para

    # # PART B
    mars_image_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(mars_image_url)
    mars_pic_html = browser.html
    soup=bs(mars_pic_html, 'html.parser')
    mars_pic = soup.find('a','fancybox')['data-fancybox-href']
    JPL_url = "https://www.jpl.nasa.gov"+mars_pic
    featured_image_url = JPL_url
    scrape_dict["featured_image_url"] = featured_image_url

    # # PART C
    mars_weather_url = "https://twitter.com/marswxreport?lang=en"
    browser.visit(mars_weather_url)
    mars_weath_html = browser.html
    soup=bs(mars_weath_html, 'html.parser')
    mars_w = soup.find('p',class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text")
    mars_weather = mars_w.text    
    scrape_dict["mars_weather"] = mars_weather

    # # PART D
    import pandas as pd
    table_url = 'https://space-facts.com/mars/'
    tables = pd.read_html(table_url)
    df=tables[0]
    html_table = df.to_html()
    scrape_dict["html_table"] = html_table

    # # PART E
    first_image_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/cerberus_enhanced"
    second_image_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/schiaparelli_enhanced"
    third_image_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/syrtis_major_enhanced"
    fourth_image_url = "https://astrogeology.usgs.gov/search/map/Mars/Viking/valles_marineris_enhanced"
    # Retrieve page with the requests module
    first_response = requests.get(first_image_url)
    # Create BeautifulSoup object; parse with 'lxml'
    first_soup = bs(first_response.text, 'html.parser')
    second_response = requests.get(second_image_url)
    second_soup = bs(second_response.text, 'html.parser')
    third_response = requests.get(third_image_url)
    third_soup = bs(third_response.text, 'html.parser')
    fourth_response = requests.get(fourth_image_url)
    fourth_soup = bs(fourth_response.text, 'html.parser')
    first_pic = first_soup.find('img','wide-image')['src']
    cerberus_url = "https://astrogeology.usgs.gov"+first_pic
    second_pic = second_soup.find('img','wide-image')['src']
    schiarelli_url = "https://astrogeology.usgs.gov"+second_pic
    third_pic = third_soup.find('img','wide-image')['src']
    syrtis_url = "https://astrogeology.usgs.gov"+third_pic
    fourth_pic = fourth_soup.find('img','wide-image')['src']
    valles_url = "https://astrogeology.usgs.gov"+fourth_pic
    hemisphere_image_urls = [
        {"title": "Valles Marineris Hemisphere", "img_url": valles_url},
        {"title": "Cerberus Hemisphere", "img_url": cerberus_url},
        {"title": "Schiaparelli Hemisphere", "img_url": schiarelli_url},
        {"title": "Syrtis Major Hemisphere", "img_url": syrtis_url}]
    scrape_dict["hemisphere_image_urls"] = hemisphere_image_urls
return scrape_dict

def index():
    mars = list(db.collection.find())
    return render_template('index.html', mars = mars)