import yaml

def load_config():
    with open(".config.yaml", 'r') as stream:
        config_yaml = yaml.safe_load(stream)

        # TODO: read from env variable
        config_yaml['base']['app']['imagesDb']['password']='mbit'
        return config_yaml