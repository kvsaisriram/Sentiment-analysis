import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import re


df = pd.read_csv('all_product_links.csv')
index = df.index
number_of_rows = len(index)
reviews2 = []

for n in range(number_of_rows):
    url = df.iloc[n,0]
    html = requests.get(url).text
    soup = bs(html,'html.parser')
    for i in range(0,4):    
            if soup.find('p',id="review-preview-toggle-{j}".format(j=i))==None:
                continue
            else:
                reviews2.append(soup.find('p',id="review-preview-toggle-{j}".format(j=i)).text)

#creating data frame for scrapped reviews
df2=pd.DataFrame(reviews2,columns=['reviews'])

def clean_reviews(review):
    return " ".join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])", " ",review.lower()).split())

df2['reviews']=df2['reviews'].apply(clean_reviews)

df2.to_csv('scrapped_reviews.csv', index=False)











