from sqlalchemy import Column, Float, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Engine
from flask import current_app

from app.config.config import DatabaseConfig

Base = declarative_base()

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(String(36), primary_key=True)
    path = Column(Text)
    date = Column(DateTime)

def add_picture(picture_id, picture_path, picture_date):
    engine = get_engine()
    print("engine: ", engine)
    Session = sessionmaker(bind=engine)
    session = Session()

    new_picture = Picture(
        id=picture_id,
        path=picture_path,
        date=picture_date
    )

    session.add(new_picture)

    session.commit()

    session.close()

def delete_picture(picture_id: str):
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    picture = session.query(Picture).get(picture_id)

    if picture:
        session.delete(picture)

        session.commit()

    session.close()

class Tag(Base):
    __tablename__ = 'tags'
    tag = Column(String(32), primary_key=True)
    picture_id = Column(String(36), primary_key=True)
    confidence = Column(Float)
    date = Column(DateTime)

def add_tag(tag_name, tag_picture_id, tag_confidence, tag_date):
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    
    new_tag = Tag(
        tag=tag_name,
        picture_id=tag_picture_id,
        confidence=tag_confidence,
        date=tag_date
    )

    session.add(new_tag)

    session.commit()

    session.close()

def delete_tag(tag_id: str):
    engine = get_engine()
    Session = sessionmaker(bind=engine)
    session = Session()

    tag = session.query(Tag).get(tag_id)

    if tag:
        session.delete(tag)

        session.commit()

    session.close()


def get_engine() -> Engine:
    try:
        engine = current_app.extensions['db_engine']
        return engine
    except KeyError:
        raise Exception("Database engine not found in app context")