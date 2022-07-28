import os
import argparse
import pandas as pd
from utils import read_params

def open_billboard(path_file):
    try:
        for file in os.listdir(path_file):
            if file.endswith('csv'):
                wkspFldr = os.path.abspath(path_file)
                print(wkspFldr)
                df = pd.read_csv(os.path.join(wkspFldr, file), sep=",")
                return df
    except:
        print("No billboard file")


def create_raw_billboard(config_path):
    config = read_params(config_path = config_path)
    dir_name = config['data_source']['Billboard']
    df_AMT_v2 = open_billboard(dir_name
    raw_AMT_v2_path = config['load_data']['raw_billboard_csv']
    df_AMT_v2.to_json(raw_AMT_v2_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    create_raw_billboard(config_path=parsed_args.config)