import numpy as np
import pandas as pd
from bs4 import BeautifulSoup
import requests
from kaggle.api.kaggle_api_extended import KaggleApi
import datetime
import os
import json

TMDB_KEY = os.getenv('TMDB_KEY')

SERIES_ID = 456
#initialize dataframes
episode_data = []

# For each season
seasons = list(range(1,35))
for season in seasons:
    print(season)
    wiki = f'https://en.wikipedia.org/wiki/The_Simpsons_(season_{season})'
    imdb = f'https://www.imdb.com/title/tt0096697/episodes?season={season}'
    
    
    #wiki
    req=requests.get(wiki)
    content=req.text
    soup=BeautifulSoup(content)
    rows=soup.findAll('tr', 'vevent')
    
    #imdb
    imdb_req=requests.get(imdb)
    imdb_content=imdb_req.text
    imdb_soup=BeautifulSoup(imdb_content)
    imdb_rows=imdb_soup.findAll('div', 'ipl-rating-star small')
    descriptions = imdb_soup.findAll('div', 'item_description')
    

    
    for index in range(len(rows)):
        ep_row = {}
        ep_row['season'] = season
        data = rows[index].findAll('td')
        ep_row['number_in_series'] = rows[index].findAll('th')[0].text.split('[')[0]
        ep_row['number_in_season'] = data[0].text
        ep_row['title'] = data[1].text.strip("\"")
        ep_row['directed_by'] = data[2].text.split('[')[0]
        ep_row['written_by'] = data[3].text.split('[')[0]
        if len(data[4].findAll('span')) > 1:
            ep_row['original_air_date'] = data[4].findAll('span')[1].text
        ep_row['production_code'] = data[5].text.split("[")[0]
        if len(data[6].text.split('[')) > 0:
            ep_row['us_viewers_in_millions'] = data[6].text.split('[')[0]
        if index < len(descriptions):
            ep_row['description'] = descriptions[index].text.split('\n')[1]

        tmdb_url = f"https://api.themoviedb.org/3/tv/{SERIES_ID}/season/{season}/episode/{data[0].text}?language=en-US&api_key={TMDB_KEY}"

        response = requests.get(tmdb_url)
        output = json.loads(response.text)
        ep_row['tmdb_rating'] = str(output['vote_average'])
        ep_row['tmdb_vote_count'] = str(output['vote_count'])

        #need imdb rating
        if index < len(imdb_rows):
            if len(imdb_rows[index].findAll('span', 'ipl-rating-star__rating')) > 0:
                rating = imdb_rows[index].findAll('span', 'ipl-rating-star__rating')[0].text
                ep_row['imdb_rating'] = rating
        
        
        episode_data.append(ep_row)

        
        
episode_data = pd.DataFrame(episode_data, columns = ['title', 'description', 'original_air_date', 
                                                     'production_code','directed_by', 'written_by', 'season', 'number_in_season', 
                                                     'number_in_series', 'us_viewers_in_millions', 'imdb_rating', 'tmdb_rating', 'tmdb_vote_count'])         


#write data
episode_data.index.name = 'id'

#Check if new data added
prev_episode_data = pd.read_csv('./data/simpsons_episodes.csv', index_col='id')

SAME = prev_episode_data.shape == episode_data.shape

#if not the same, update
if not SAME:
    episode_data.to_csv('./data/simpsons_episodes.csv')
    api = KaggleApi()
    api.authenticate()

    api.dataset_create_version(
    "./data/",
    version_notes=f"Updated on {datetime.datetime.now().strftime('%Y-%m-%d')}",
    )