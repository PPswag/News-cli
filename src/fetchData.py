from newspaper import Article
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
from news import *
import datetime
from transformers import *

def summarize(text, per):
    
    nlp = spacy.load('en_core_web_sm')
    doc= nlp(text)
    word_frequencies={}
    for word in doc:
        if word.text.lower() not in list(STOP_WORDS):
            if word.text.lower() not in punctuation:
                if word.text not in word_frequencies.keys():
                    word_frequencies[word.text] = 1
                else:
                    word_frequencies[word.text] += 1
    max_frequency=max(word_frequencies.values())
    for word in word_frequencies.keys():
        word_frequencies[word]=word_frequencies[word]/max_frequency
    sentence_tokens= [sent for sent in doc.sents]
    sentence_scores = {}
    for sent in sentence_tokens:
        for word in sent:
            if word.text.lower() in word_frequencies.keys():
                if sent not in sentence_scores.keys():
                    sentence_scores[sent]=word_frequencies[word.text.lower()]
                else:
                    sentence_scores[sent]+=word_frequencies[word.text.lower()]
    select_length=int(len(sentence_tokens)*per)
    summary=nlargest(select_length, sentence_scores,key=sentence_scores.get)
    final_summary=[word.text for word in summary]
    summary=''.join(final_summary)
    return summary

# url = 'http://fox13now.com/2013/12/30/new-year-new-laws-obamacare-pot-guns-and-drones/'
# Fetch data
query = 'burgers'
responseDict = {}
responseList = []
every = news.get_everything(query)
info = news.fetch_all_genesis_url(every['articles'])
for i in range(0, 5):
    url = every['articles'][i]['url']
    article = Article(url)

    article.download()
    article.parse()
    title = article.title if article.title else "Unknown"
    authors = ', '.join(article.authors) if article.authors else "Unknown"
    publish_date = article.publish_date if article.publish_date else "Unknown"
    summary = summarize(article.text, 0.3)
    responseDict['title'] = title
    responseDict['author'] = authors
    responseDict['url'] = url
    responseDict['summary'] = summary
    responseDict['publish_date'] = publish_date
    responseList.append(responseDict)
print(responseList)