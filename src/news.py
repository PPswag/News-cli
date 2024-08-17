import requests
import base64
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


    def fetch_decoded_batch_execute(self, id):
        s = (
            '[[["Fbv4je","[\\"garturlreq\\",[[\\"en-US\\",\\"US\\",[\\"FINANCE_TOP_INDICES\\",\\"WEB_TEST_1_0_0\\"],'
            'null,null,1,1,\\"US:en\\",null,180,null,null,null,null,null,0,null,null,[1608992183,723341000]],'
            '\\"en-US\\",\\"US\\",1,[2,3,4,8],1,0,\\"655000234\\",0,0,null,0],\\"' +
            id +
            '\\"]",null,"generic"]]]'
        )

        headers = {
            "Content-Type": "application/x-www-form-urlencoded;charset=utf-8",
            "Referer": "https://news.google.com/"
        }

        response = requests.post(
            "https://news.google.com/_/DotsSplashUi/data/batchexecute?rpcids=Fbv4je",
            headers=headers,
            data={"f.req": s}
        ) # orginally wanted to use post, but it didn't work, thankfully this code showed me

        if response.status_code != 200:
            raise Exception("Failed to fetch data from Google.")

        text = response.text
        header = '[\\"garturlres\\",\\"'
        footer = '\\",'
        if header not in text:
            raise Exception(f"Header not found in response: {text}")
        start = text.split(header, 1)[1]
        if footer not in start:
            raise Exception("Footer not found in response.")
        url = start.split(footer, 1)[0]
        return url

    def decode_google_news_url(self, source_url): 
        # I copied this code, after using selnium, thanks to Huskley
        url = requests.utils.urlparse(source_url)
        path = url.path.split("/")
        if url.hostname == "news.google.com" and len(path) > 1 and path[-2] == "articles":
            base64_str = path[-1]
            decoded_bytes = base64.urlsafe_b64decode(base64_str + '==')
            decoded_str = decoded_bytes.decode('latin1')

            prefix = b'\x08\x13\x22'.decode('latin1')
            if decoded_str.startswith(prefix):
                decoded_str = decoded_str[len(prefix):]

            suffix = b'\xd2\x01\x00'.decode('latin1')
            if decoded_str.endswith(suffix):
                decoded_str = decoded_str[:-len(suffix)]

            bytes_array = bytearray(decoded_str, 'latin1')
            length = bytes_array[0]
            if length >= 0x80:
                decoded_str = decoded_str[2:length+1]
            else:
                decoded_str = decoded_str[1:length+1]

            if decoded_str.startswith("AU_yqL"):
                return self.fetch_decoded_batch_execute(base64_str)

            return decoded_str
        else:
            return source_url

    def fetch_all_genesis_url(self, url) -> List[str]:
        x = len(url)
        genesis_url = []

        for i in range(x):
            decoded_url = self.decode_google_news_url(url[i]['url'])
            genesis_url.append(decoded_url)
        return genesis_url





news = News("e46d3ebc97c14f2eb35fe9ffb8ea328a")
info = news.get_top_headlines('us', 'business')
source = news.fetch_all_genesis_url(info['articles'])
print(source)
# for i in range(0, 5):
#     source_url = info['articles'][i]['url']
#     decoded_url = news.decode_google_news_url(source_url)

#     print(decoded_url)

# info = news.fetch_top_headlines('us', 'business')
# query = 'bitcoin'
# every = news.get_everything(query)




'''
    json = {
        "title": page_title, 
        "author": author,
        "url": actual_url,
        "summary": "summary ( given by article newspaper package)"
    }

    csv = basically like json, but better format
'''


