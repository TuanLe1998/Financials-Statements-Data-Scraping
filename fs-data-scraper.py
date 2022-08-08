import pandas as pd
import numpy as np
import bs4 as bs
from bs4 import BeautifulSoup
import requests
import re

# In this project we will try with Vinatrans, a big logistics company in Viet Nam

# Get the base url used for scraping by inputing the listing code
listing_code = 'VIN'


def get_url(listing_code):
    base_url = 'https://s.cafef.vn/bao-cao-tai-chinh/{}/IncSta/2023/1/0/0/bao-cao-tai-chinh-cong-ty-co-phan-tap-doan-hoa-phat.chn'.format(
        listing_code)
    return base_url


url = get_url(listing_code=listing_code)

# Initiate the soup using the url generated above


def initiate_soup(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup


soup = initiate_soup(url)

# Scrape the columns names
header = ['Hạng mục']


def get_table_name(soup):
    header_table_info = soup.findAll('table')[2].findAll('tr')
    for column_name in header_table_info[0].findAll('td', attrs={'class': 'h_t'}):
        header.append(column_name.text.strip())


get_table_name(soup)

# Scrape the data
all_data = []
for row in soup.findAll('table')[3].findAll('tr'):
    for data in row.findAll('td', attrs={'class': 'b_r_c'}):
        all_data.append(data.text.strip())

all_data = []
for row in soup.findAll('table')[3].findAll('tr'):
    row_data = [x.text.strip()
                for x in row.findAll('td', attrs={'class': 'b_r_c'})]
    all_data.append(row_data)

all_data = [x for x in all_data if x != []]

# Create dataframe to store the data
df = pd.DataFrame(columns=header)
for data in all_data:
    df.loc[len(df)] = data[:5]
df.set_index('Hạng mục', inplace=True)

# Transpose the dataframe for easier visualization
df = df.transpose()

# Save to local folder
df.to_csv(listing_code+'.csv')
