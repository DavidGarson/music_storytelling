import os
import argparse
import pandas as pd
from utils import read_params

def open_raw_riaa(path_file):
    try:
        if os.path.exists(path_file):
            wkspFldr = os.path.abspath(path_file)
            df = pd.read_csv(wkspFldr, sep=";")
            return df
    except:
        print("No raw riaa file")

def cleansing_df(df, min_year):
    df["artist"]=df["artist"].str.lower()
    df["song"]=df["song"].str.lower()
    df=df.drop_duplicates(subset=['artist', 'song'])
    #remove Latin music
    filter = 'type!="Latin"'
    filter_genre = 'genre!="LATIN"'
    df = df.query(filter)
    df = df.query(filter_genre)
    #calcul date diff
    df['certificat_gold_date'] = pd.to_datetime(df['certificat_gold_date'])
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['Valid'] = [True if (cert - rel).days>=365*min_year else False for rel, cert in zip(df['release_date'], df['certificat_gold_date'])]
    # keep song with valid criteria
    filter_valid = 'Valid==True'
    df = df.query(filter_valid)
    return df

def create_riaa_dataset(config_path):
    config = read_params(config_path = config_path)
    dir_name = config['load_data']['raw_riaa_csv']
    min_year = config['study']['min_year_to_get_certification']
    df = open_raw_riaa(dir_name)
    cleansing_df(df,min_year)
    #raw_AMT_v2_path = config['load_data']['raw_billboard_csv']
    #df.to_csv(raw_AMT_v2_path)
    print(df)
if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    create_riaa_dataset(config_path=parsed_args.config)