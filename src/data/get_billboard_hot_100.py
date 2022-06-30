import os
import argparse
import kaggle
from utils import read_params

def get_billboard_hot_100(config_path):
    config = read_params(config_path)
    kaggle_dataset = config['kaggle']['dataset']
    save_path = config['data_source']['Billboard']
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(kaggle_dataset, path=save_path, unzip=True)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="config/params.yaml")
    parsed_args = args.parse_args()
    get_billboard_hot_100(config_path=parsed_args.config)