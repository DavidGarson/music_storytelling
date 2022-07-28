import argparse
import json
import discogs_client

from tqdm import trange, tqdm
from timeit import default_timer as timer
from datetime import timedelta
import time
import pandas as pd

from random import random
from utils import read_params

def create_discogs_client(my_token):
    d = discogs_client.Client('ExampleApplication/0.1', user_token=my_token)
    return d


def songs_extract(discogs_client, begin_year, end_year, genre, country):
    d = discogs_client
    # start = timer()
    df_final = pd.DataFrame(columns=['artist', 'songs', 'year', 'country', 'genre','label'])


    for year in trange(begin_year, end_year+1, 1, desc='year loop'):
        # mid_start = timer()
        results= d.search(type='release', genre=genre, country=country, year=year) #'Pop'
        cols = ['artist', 'songs', 'year', 'country', 'genre', 'label']
        df2 = pd.DataFrame(columns=cols, index=range(results.pages))
        df_final = []
        for i in trange(results.pages, desc='page loop'):
            time.sleep(2*random())  #slow the program to limit impact on API
            df2.loc[i].artist = results[i].artists[0].name
            df2.at[i,'songs'] = results[i].tracklist
            df2.loc[i].year = results[i].year
            df2.loc[i].country = results[i].country
            df2.loc[i].genre = results[i].genres[0]
            df2.loc[i].label = results[i].labels[0]
        df2 = df2.explode('songs', ignore_index=True)
        df_final.append(df2)
            #df_final = df_final.append(df2, ignore_index=True)
        # mid_time = timer()
        print(f"year {year} done, {df2.shape[0]} {genre} songs extracted") # in {timedelta(seconds=mid_time-mid_start)}")
    df_final = pd.concat(df_final)
    #extract title in each song
    for i in trange(len(df_final.songs), desc='title cleaning loop'):
        df_final.songs[i] = df_final.songs[i].title
    # end = timer()
    
    # print(f"the extraction took a total of {timedelta(seconds=end-start)}")
    return df_final


def get_discogs_token(config_path):
    f = open(config_path)
    token = json.load(f)
    f.close()
    return token


def get_discogs(config_path):
    config = read_params(config_path)
    save_path = config['data_source']['Discogs']
    token_path = config['discogs']['token']
    begin_year_study = config['study']['begin_year']
    end_year_study = config['study']['end_year']
    music_genres = config['study']['music_genres']
    country = config['study']['country']

    my_token =  get_discogs_token(token_path)
    d = create_discogs_client(my_token)

    for genre in tqdm(music_genres.values(), desc='genre loop'):
        print(f"********* {genre} *********")
        #print(f"{save_path}/discogs_{begin_year_study}_{genre.lower().replace(' ','_')}.json")
        df_temp = songs_extract(d, begin_year_study, end_year_study, genre, country)   
        file_path_save = f"{save_path}/discogs_{begin_year_study}_{genre.lower().replace(' ','_')}.csv" 
        df_temp.to_csv(file_path_save,sep=';', index=False)
        print(f"********* {genre} completed *********\n")
    print("extraction completed")

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="config/params.yaml")
    parsed_args = args.parse_args()
    get_discogs(config_path=parsed_args.config)