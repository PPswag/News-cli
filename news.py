import requests
import json
import nltk
from textblob import TextBlob
from newspaper import Article
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import time
from typing import List

class News:

    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "https://newsapi.org/v2"

    def get_top_headlines(self, country, category):
        url = f"{self.base_url}/top-headlines?country={country}&category={category}&apiKey={self.api_key}"
        response = requests.get(url) # simple code to get the top headlines
        return response.json()
    def get_everything(self, query):
        url = f"{self.base_url}/everything?q={query}&apiKey={self.api_key}"
        response = requests.get(url)
        return response.json()
    
    def fetch_top_headlines(self, country: str, category: str) -> List[str]:
        info = self.get_top_headlines(country, category)
        urls = [article.get('url') for article in info.get('articles', [])]
        listed_url = []
        for url in urls[0:7]:
            chrome_options = Options()
            chrome_options.add_argument("--headless") 
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage") # speed up the process, don't need to open up chrome
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)


            driver.get(url)

            try:
                element = WebDriverWait(driver, 4).until(EC.presence_of_element_located((By.TAG_NAME, "p"))
                )


                actual_url = driver.current_url

                page_title = driver.title
                print(f"Actual URL: {actual_url}") 
                listed_url.append(actual_url)
            except Exception as e:
                print("null: sadly this url is experiencing some issues")
            finally:
                driver.quit()
        return listed_url



news = News("e46d3ebc97c14f2eb35fe9ffb8ea328a")
info = news.fetch_top_headlines('us', 'business')
print(info)



'''
    json = {
        "title": page_title, 
        "author": author,
        "url": actual_url,
        "summary": "summary ( given by article newspaper package)"
    }

    csv = basically like json, but better format
'''


