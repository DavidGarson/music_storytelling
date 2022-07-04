from importlib.resources import path
import pandas as pd
import os
import argparse
from utils import read_params


def open_exclud_AMT_file(path_file):
    file_ref = 'exclud_AMT.txt'
    if os.path.exists(path_file):
        df_ID_AMT_EXCLU = pd.read_csv(path_file, sep = ',').T
        df_ID_AMT_EXCLU.reset_index(inplace=True)
    else:
        wkspFldr = os.path.dirname(path_file)
        with open(os.path.join(wkspFldr, file_ref), 'w') as f:
            pass
        df_ID_AMT_EXCLU = pd.DataFrame(columns = ['index'])
    
    return df_ID_AMT_EXCLU

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

def create_exclusion_file(config_path):
    config = read_params(config_path)
    AMT_V2_dataset = config['data_source']['AMT_V2']
    save_path = config['load_data']['exclud_AMT']
    list_already_excluded = open_exclud_AMT_file(save_path)
    print(list_already_excluded)
    # df_AMT_V2 = open_AMT_V2_answer(AMT_V2_dataset)
    # full_exclud = df_AMT_V2['MID'].unique()
    # full_exclud = full_exclud.tolist()

    # full_exclud.extend(list_already_excluded['index'].tolist())
    # result = [s.strip() for s in full_exclud]
    # result = list(set(result))
    # print(len(result))
    # with open(save_path, 'w') as f:
    #     f.writelines(", ".join(str(x) for x in result))


if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    create_exclusion_file(config_path=parsed_args.config)