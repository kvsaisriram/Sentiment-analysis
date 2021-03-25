from bs4 import BeautifulSoup as bs
import requests
from selenium import webdriver
import pandas as pd 
import time
"""====X==== PART-ONE ====X===="""
# Here we are changing the page no. of one link that we have, and storing it in a list to further visit
# each link to collect all the product links from each 250 page
link=[]
for i in range(1,251):
    link.append('https://www.etsy.com/in-en/c/jewelry/earrings/ear-jackets-and-climbers?ref=pagination&page={j}'.format(j=i))
    
    
""" This part of the code can be further changed, we might wanna avoid openning and closing our browser 250 times to
    get all the product links i could have done it but it worked, so never mind..!                     """
    
# Here we are visiting each 250 page and collecting the product links   
all_product_links=[]   
for i in range(0,250): 
    links = link[i]
    driver = webdriver.Firefox()
    driver.get(links)
    page = driver.page_source
    page_soup = bs(page,"html.parser")
    #getting all the anchor tags with href attributes that has all the 64 links 
    hlinks = [a['href'] for a in page_soup.find_all('a', href=True)]
    #puttin all the links in the list so that we can travers each one of them and get the reviews
    match = [s for s in hlinks if "listing" in s]
    all_product_links.extend(match)
    driver.close()
    
    
df=pd.DataFrame(all_product_links,columns=['all_product_links']) #converting our list to a dataframe

df.shape                                      #might wanna look at our data to get a birds eye view

df.to_csv('all_product_links.csv', index=False)
