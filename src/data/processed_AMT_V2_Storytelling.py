from importlib.resources import path
import pandas as pd
import numpy as np
import os
import argparse
from utils import read_params, merge

def table_score_creation(df, score):
    # print(df)
    df_transpose = df.T
    df_transpose = df_transpose.reset_index().rename_axis(None, axis=1)
    # print(df_transpose)
    df_transpose.iloc[:,1:] = df_transpose.iloc[:,1:].astype(float)
    df_transpose['score'] = df_transpose.iloc[:,1:].mean(axis = 1, skipna=True)
    df_transpose[['song_id', 'Q_id']] = df_transpose['index'].str.split('_', 1, expand=True)
    df_transpose.drop(columns=['index'], axis=1,inplace=True, )
    df_analyse = df_transpose[['song_id', 'Q_id','score']]
    table = pd.pivot_table(df_analyse, index='song_id',columns='Q_id', aggfunc=np.sum, dropna=True)
    table.reset_index(inplace=True)
    table['eval_score'] = table.iloc[:,score].mean(axis = 1, skipna=True)
    table.columns = table.columns.map('|'.join).str.strip('|')
    table['song_id'] = table['song_id'].str[1:].astype(int)
    # eval storytelling
    conditions = [
    (table['eval_score'] <= table['eval_score'].mean()-table['eval_score'].std()),
    (table['eval_score'] >= table['eval_score'].mean()+table['eval_score'].std()),
    (table['eval_score'] > table['eval_score'].mean()-table['eval_score'].std()) & (table['eval_score'] < table['eval_score'].mean()+table['eval_score'].std())
    ]

    values = ['No', 'Yes', 'UNK']

    table['storytelling'] = np.select(conditions, values)
    
    return table


def cleaning_AMT_V2(df, dict):
    df.drop(axis=0, index=0,inplace=True)
    df.reset_index(drop=True, inplace=True)
    df = df.dropna(subset=['random']).copy()
    df.reset_index(drop=True, inplace=True)
    df.rename(columns = dict, inplace = True)
    df_cleaned = df[df['MID'].astype(str).str.startswith('A')]
    return df_cleaned


def processed_AMT_V2(config_path):
    config = read_params(config_path)
    AMT_V2_dataset  = config['load_data']['raw_AMT_v2_json']
    hiphop_mapping_dict = config['AMT_v2_mapping']['hiphop_mapping_dict']
    pop_mapping_dict = config['AMT_v2_mapping']['pop_mapping_dict']
    Q_for_score = config['AMT_v2_score_storytelling']['lst_questions_used_score']
    path_processed_AMT_V2_hiphop = config['processed_data']['processed_AMT_V2_storytelling_hiphop_csv']
    path_processed_AMT_V2_pop = config['processed_data']['processed_AMT_V2_storytelling_pop_csv']

    df_AMT_V2 = pd.read_json(AMT_V2_dataset)
    merge_dict = {**hiphop_mapping_dict, **pop_mapping_dict}
    cleaned_AMT_V2 = cleaning_AMT_V2(df_AMT_V2, merge_dict)
    whole_dataframes = {}
    whole_dataframes["hiphop"] = cleaned_AMT_V2.loc[:, cleaned_AMT_V2.columns.str.startswith('H')]
    whole_dataframes["pop"] = cleaned_AMT_V2.loc[:, cleaned_AMT_V2.columns.str.startswith('P')]

    df_processed_AMT_V2_hiphop = table_score_creation(whole_dataframes["hiphop"], Q_for_score)
    df_processed_AMT_V2_pop = table_score_creation(whole_dataframes["pop"], Q_for_score)
    df_processed_AMT_V2_hiphop.to_csv(path_processed_AMT_V2_hiphop)
    df_processed_AMT_V2_pop.to_csv(path_processed_AMT_V2_pop)


if __name__=="__main__":
    args = argparse.ArgumentParser()
    default_config_path = os.path.join("config", "params.yaml")
    args.add_argument("--config", default=default_config_path)
    parsed_args = args.parse_args()
    processed_AMT_V2(config_path=parsed_args.config)