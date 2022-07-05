import yaml


def read_params(config_path):
    with open(config_path) as yaml_file:
        config = yaml.safe_load(yaml_file)
    return config

def merge(dict1, dict2):
    return(dict1.update(dict2))