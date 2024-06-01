from flask import current_app
from sqlalchemy import Column, Float, String, Text, DateTime, func
from sqlalchemy.ext.declarative import declarative_base
from flask_sqlalchemy import SQLAlchemy

Base = declarative_base()
db = SQLAlchemy(model_class=Base)

class Picture(Base):
    __tablename__ = 'pictures'
    id = Column(String(36), primary_key=True)
    path = Column(Text)
    date = Column(DateTime)

def add_picture(picture_id, picture_path, picture_date):
    new_picture = Picture(
        id=picture_id,
        path=picture_path,
        date=picture_date
    )

    db.session.add(new_picture)
    db.session.commit()
    db.session.close()

def get_picture_with_tags(picture_id: str):
    # the tag information should be formatted as a list of dictionaries [{tag: <tag>, confidence: <confidence>}]
    picture = db.session.query(
        Picture.id,
        Picture.path,
        Picture.date,
        func.aggregate_strings(Tag.tag, ',').label('tags'),
        func.aggregate_strings(Tag.confidence, ',').label('confidences')
    ).filter(
        Picture.id == picture_id
    ).filter(
        Picture.id == Tag.picture_id
    ).group_by(Picture.id).first()

    current_app.logger.info(f"picture: {picture}")


    db.session.close()

    return picture

def get_pictures_with_tags(min_date, max_date, tags):
    # min_date and max_date are datetime objects and tags is a list of strings
    # all can be None
    # group by picture_id

    filter_results_num = 0 if not tags else len(tags)

    results = db.session.query(
        Picture.id,
        Picture.path,
        Picture.date,
        func.aggregate_strings(Tag.tag, ',').label('tags'),
        func.aggregate_strings(Tag.confidence, ',').label('confidences')
    ).filter(
        Picture.id == Tag.picture_id
    ).filter(
        Picture.date >= min_date if min_date else True
    ).filter(
        Picture.date <= max_date if max_date else True
    ).filter(
        Tag.tag.in_(tags) if tags else True
    ).group_by(Picture.id)
    
    if filter_results_num: 
        results =results.having(func.count(Picture.id) == filter_results_num)
    
    results.all()

    db.session.close()

    return results

def delete_picture(picture_id: str):
    picture = db.session.query(Picture).get(picture_id)

    if picture:
        db.session.delete(picture)
        db.session.commit()

    db.session.close()

class Tag(Base):
    __tablename__ = 'tags'
    tag = Column(String(32), primary_key=True)
    picture_id = Column(String(36), primary_key=True)
    confidence = Column(Float)
    date = Column(DateTime)

def add_tag(tag_name, tag_picture_id, tag_confidence, tag_date):
    new_tag = Tag(
        tag=tag_name,
        picture_id=tag_picture_id,
        confidence=tag_confidence,
        date=tag_date
    )

    db.session.add(new_tag)
    db.session.commit()
    db.session.close()

def delete_tag(tag_id: str):
    tag = db.session.query(Tag).get(tag_id)

    if tag:
        db.session.delete(tag)
        db.session.commit()

    db.session.close()

def get_tags(min_date, max_date):
    results = db.session.query(
        Tag.tag,
        func.count(Tag.picture_id).label('n_images'),
        func.min(Tag.confidence).label('min_confidence'),
        func.max(Tag.confidence).label('max_confidence'),
        func.avg(Tag.confidence).label('mean_confidence')
    ).filter(
        Tag.date >= min_date if min_date else True
    ).filter(
        Tag.date <= max_date if max_date else True
    ).group_by(Tag.tag).all()

    return results