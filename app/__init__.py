from pickle import GLOBAL
from flask import Flask
from alembic.config import Config as AlembicConfig
from alembic import command
from sqlalchemy import create_engine
from .config.config import load_config, DatabaseConfig
from .model import db
from . import views

def create_app():
    # load config
    config = load_config()

    # inject database config into alembic
    run_migrations(config.app.database)

    app = Flask(__name__)
    app.register_blueprint(views.bp)
    app.config['config'] = config
    # configure the database
    app.config["SQLALCHEMY_DATABASE_URI"] = db_connection_string(config.app.database)
    # initialize the app with the extension
    db.init_app(app)

    return app


def run_migrations(config: DatabaseConfig):
    """Runs the pending schema migration steps

    Args:
        config: the database config needed to perform the migration
    """

    # Set up migrator config
    migrationConfig = AlembicConfig('alembic.ini')
    migrationConfig.set_main_option('sqlalchemy.url', db_connection_string(config))
    migrationConfig.set_main_option('script_location', config.alembic_path)
    # Create a SQLAlchemy engine
    print("Database: ", migrationConfig.get_main_option('sqlalchemy.url'))
    engine = create_engine(migrationConfig.get_main_option('sqlalchemy.url'))

    with engine.connect() as conn:
        print("Current revision: ", command.current(config=migrationConfig))
        print("Running pending migrations...")
        command.upgrade(migrationConfig, 'head')
        print("Finished migrating database. Current version is set to :", command.current(config=migrationConfig))


def db_connection_string(config: DatabaseConfig):
    return f"{config.driver}://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}"

app = create_app()