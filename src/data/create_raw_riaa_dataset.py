import os
import argparse
import pandas as pd
from utils import read_params

def create_riaa_raw_dataset(config_path):
    config = read_params(config_path = config_path)
    dir_name = config['data_source']['RIAA']
    df_list = []
    # df_riaa = pd.DataFrame()
    
    for file in os.listdir(dir_name):
        if file.endswith('csv'):
            df_path = os.path.join(dir_name, file)
            df = pd.read_csv(df_path, sep = ';', encoding='latin-1')
            df_list.append(df)
    csv_merged = pd.concat(df_list, ignore_index=True)
    new_cols = [col.replace(" ","_") for col in csv_merged.columns]
    raw_riaa_path = config['load_data']['raw_riaa_csv']
    csv_merged.to_csv(raw_riaa_path,sep=';', index=False,header=new_cols)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    create_riaa_raw_dataset(config_path=parsed_args.config)