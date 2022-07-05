import os
import argparse
import pandas as pd
from utils import read_params

def open_AMT_V2_answer(path_file):
    try:
        for file in os.listdir(path_file):
            if file.endswith('xlsx'):
                wkspFldr = os.path.abspath(path_file)
                print(wkspFldr)
                df_AMT = pd.read_excel(os.path.join(wkspFldr, file), sheet_name=0, engine="openpyxl")
                # print(type(df_AMT))
                return df_AMT
    except:
        print("No AMT_V2 file")


def create_raw_AMT_v2_dataset(config_path):
    config = read_params(config_path = config_path)
    dir_name = config['data_source']['AMT_V2']
    df_AMT_v2 = open_AMT_V2_answer(dir_name)
    raw_AMT_v2_path = config['load_data']['raw_AMT_v2_json']
    df_AMT_v2.to_json(raw_AMT_v2_path)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    create_raw_AMT_v2_dataset(config_path=parsed_args.config)