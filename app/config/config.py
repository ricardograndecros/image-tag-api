import yaml

def load_config():
    with open(".config.yaml", 'r') as stream:
        config_yaml = yaml.safe_load(stream)
        return config_yaml