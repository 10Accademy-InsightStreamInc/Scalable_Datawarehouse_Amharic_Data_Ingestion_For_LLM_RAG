import requests
from bs4 import BeautifulSoup
import pandas as pd
import psycopg2
from psycopg2 import sql
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
import logging

#logger = logging.getLogger(__name__)

#formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s')

#filehandler = logger.FileHandler('log.log')
#filehandler.setLevel(logging.INFO)
#filehandler.setFormatter(formatter)

#logger.addHandler(filehandler)

def scrape_new(base_url: str, num_pages: int):#, elements: list, name: list, link=True) - > pandas.DataFrame:

    """
    Returns a pandas DataFrame scraped data

    Args:
        url(str): The link to be scraped.
        elements(list)L The list of html tag to be scrapped.

    Returns:
        pd.DataFrame: A pandas DataFrame
    """

    #try:

    url_page = base_url + '?page={}'

    for page_num in range(1, num_pages+1):
        url = url_page.format(page_num)

        response = requests.get(url)

        soup = BeautifulSoup(response.content, 'html.parser')

        headlines = soup.find_all('h2')

        data_list=[]

        for headline in headlines:

            entry_list={}

            entry_list['Headlines'] = headline.get_text()

            article_link = headline.find('a')['href']

            article_response = requests.get(article_link)

            article_soup = BeautifulSoup(article_response.content, 'html.parser')

            article_body = article_soup.find(class_='bbc-fa0wmp')
            
            bodies = article_body.find_all('p')

            article_body_inse = ''

            for body in bodies:
                texts = body.get_text()

                article_body_inse+=texts

            entry_list['Body'] = article_body_inse

            date = soup.find('time')

            entry_list['Date'] = date.get_text()


            data_list.append(entry_list)

        


    return pd.DataFrame(data_list)



