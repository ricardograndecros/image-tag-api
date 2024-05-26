import os
from flask import Flask, appcontext_popped
from alembic.config import Config
from alembic import command
from sqlalchemy import create_engine, text
from .config.config import load_config
from . import views

def create_app():
    # load config
    config = load_config()

    appConfig = config['base']['app']

    # inject database config into alembic
    dbConfig = appConfig['imagesDb']
    run_migrations(dbConfig)

    # migrate database

    app = Flask(__name__)
    app.register_blueprint(views.bp)

    return app


def run_migrations(config):
    """Runs the pending schema migration steps

    Args:
        config: the database config needed to perform the migration
    """

    # Set up migrator config
    migrationConfig = Config('alembic.ini')
    migrationConfig.set_main_option('sqlalchemy.url', f"{config['driver']}://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}")
    migrationConfig.set_main_option('script_location', config['alembicPath'])
    # Create a SQLAlchemy engine
    print("Database: ", migrationConfig.get_main_option('sqlalchemy.url'))
    engine = create_engine(migrationConfig.get_main_option('sqlalchemy.url'))

    with engine.connect() as conn:
        command.downgrade(migrationConfig, 'base')
        print("Current revision: ", command.current(config=migrationConfig))
        print("Running pending migrations...")
        command.upgrade(migrationConfig, 'head')
        print("Finished migrating database. Current version is set to :", command.current(config=migrationConfig))



# Remove when using waitress
app = create_app()