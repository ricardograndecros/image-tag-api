import yaml

class DatabaseConfig:
    alembic_path:str = ""
    driver:str = ""
    database:str = ""
    host:str = ""
    port:int = 3306
    user:str = ""
    password:str = ""

    def __init__(self, config:dict):
        self.alembic_path = config.get('alembicPath')
        self.driver = config.get('driver')
        self.database = config.get('database')
        self.host = config.get('host')
        self.port = int(config.get('port'))
        self.user = config.get('user')
        self.password = config.get('password')
        
class ExternalApiConfig:
    api_key:str = ""
    api_secret:str = ""
    api_url:str = ""

    def __init__(self, config:dict):
        self.api_key = config.get('apiKey')
        self.api_secret = config.get('apiSecret')
        self.api_url = config.get('apiUrl')

class ImageStoreConfig:
    path:str = ""

    def __init__(self, config:dict):
        self.path = config.get('path')

class AppConfig(object):
    log_level:str = "debug"
    externalApis:list[ExternalApiConfig] = None
    database:DatabaseConfig = None
    image_store:ImageStoreConfig = None

    def __init__(self, config:dict):
        self.log_level = config.get('logLevel')
        self.externalApis = {api_name:ExternalApiConfig(api_config) for api_name, api_config in config.get('externalApis').items()}
        self.database = DatabaseConfig(config.get('database'))
        self.image_store = ImageStoreConfig(config.get('imageStore'))

class Config(object):
    environment:str = "dev"
    app:AppConfig = None

    def __init__(self, config:dict):
        self.environment = config.get('environment')
        self.app = AppConfig(config.get('app'))
    
def load_config():
    with open(".config.yaml", 'r') as stream:
        try:
            cfg = Config(yaml.safe_load(stream))
            return cfg
        except yaml.YAMLError as exc:
            print(exc)
            return None