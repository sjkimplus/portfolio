# -*- coding: utf-8 -*-
"""NYT_textbody.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1PMvQj8bI9bKX1SlOQQewsaDVnchANzHk
"""

import os
import time
import pandas as pd
import requests
from bs4 import BeautifulSoup
from google.colab import drive
drive.mount('/content/drive')

# directory
DIR= "/content/drive/My Drive/HCDS_Ass 3&4/"
filename = DIR+'NewYorkTimes2.csv'

df_collected_articles = pd.read_csv(filename)
df_collected_articles

array_article_urls = df_collected_articles['web_url']
array_article_urls

# to make ny time think that this request is coming from humans and not a bot
headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}

# use the first article
url = array_article_urls[0]
response = requests.get(url, headers=headers)
response

def retrieve_article(url):
    headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'}
    response = requests.get(url, headers=headers)
    return response

def extract_article_text(response):
    soup = BeautifulSoup(response.content,'lxml')
    l_paragraph = soup.select('p.evys1bk0')
    full_text = ''
    for p in l_paragraph:
        full_text += p.text + ' '
    full_text = full_text[:-1]
    return full_text

l_article_text = []
counter = 1
for i in array_article_urls:
    article_html = retrieve_article(i)
    article_text = extract_article_text(article_html)
    if counter%10==0:
      print('Retrieved and Procssed Article #{}'.format(counter))
    time.sleep(1)
    counter += 1
    l_article_text.append(article_text)

df_collected_articles['Body'] = l_article_text
df_collected_articles

new_filename = DIR + 'NewYorkTimes2_updated.csv'
df_collected_articles.to_csv(new_filename, index=False)
df_collected_articles.head()

print(len(l_article_text))

#number of text body that we could not collect
cnt=0
for l in l_article_text:
  if len(l)==0:
    cnt+=1
cnt

