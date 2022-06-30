import os
import yaml
import pandas as pd
import argparse
import kaggle






def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config


def get_billboard_hot_100(config_path):
    config = read_params(config_path)
    kaggle_dataset = config['kaggle']['dataset']
    save_path = config['data_source']['Billboard']
    print(kaggle_dataset)
    kaggle.api.authenticate()
    kaggle.api.dataset_download_files(kaggle_dataset, path=save_path, unzip=True)

if __name__=="__main__":
    args = argparse.ArgumentParser()
    args.add_argument("--config", default="config/params.yaml")
    parsed_args = args.parse_args()
    get_billboard_hot_100(config_path=parsed_args.config)