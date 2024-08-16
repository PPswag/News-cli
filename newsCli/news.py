import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from typing import List
from fileConvert import *

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
        """
        Fetches the top headlines for a given country and category.

        Args:
            country (str): The country for which to fetch headlines.
            category (str): The category for which to fetch headlines.

        Returns:
            List[str]: A list of URLs for the top headlines.
        """
        # Get the top headlines from the News API
        info = self.get_top_headlines(country, category)

        # Extract the URLs and titles of the top headlines
        urls = [article.get('url') for article in info.get('articles', [])]
        title = [article.get('title') for article in info.get('articles', [])]

        listed_url = []
        for url in urls[0:7]:
            chrome_options = Options()
            chrome_options.add_argument("--headless")  # Run Chrome in headless mode
            chrome_options.add_argument("--disable-gpu")
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")  # Speed up the process, don't need to open up chrome

            # Create a Chrome webdriver with the specified options
            driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

            # Open the URL in the webdriver
            driver.get(url)

            try:
                # Wait for the presence of a <p> tag on the page
                element = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.TAG_NAME, "p"))
                )

                # Get the current URL after any redirections
                actual_url = driver.current_url

                print(f"Actual URL: {actual_url}")  # Print the actual URL
                listed_url.append(actual_url)  # Add the URL to the list
            except Exception as e:
                print("Null")
            finally:
                driver.quit()  # Close the webdriver

        return listed_url



news = News("e46d3ebc97c14f2eb35fe9ffb8ea328a")
# info = news.fetch_top_headlines('us', 'business')
query = 'bitcoin'
every = news.get_everything(query)
# print(every)
# print(info)



'''
    json = {
        "title": page_title, 
        "author": author,
        "url": actual_url,
        "summary": "summary ( given by article newspaper package)"
    }

    csv = basically like json, but better format
'''


