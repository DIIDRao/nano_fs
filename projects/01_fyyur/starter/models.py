from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ARRAY, ForeignKey

db = SQLAlchemy()
#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String))
    shows = db.relationship('Shows', backref = 'venues')

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - done

class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    # address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    genres = db.Column(ARRAY(db.String))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_description = db.Column(db.String(120))
    shows = db.relationship('Shows', backref = 'artists')

class Shows(db.Model):
    __tablename__ = 'Shows'

    id = db.Column(db.Integer, primary_key=True)
    # venue_name = db.Column(db.String)
    # artist_name = db.Column(db.String)
    # artist_image_link = db.Column(db.String(120))
    # venue_image_link = db.Column(db.String(120))
    start_time = db.Column(db.DateTime, nullable=False)
    venue_id = db.Column(db.Integer, ForeignKey('Venue.id'))
    artist_id = db.Column(db.Integer, ForeignKey('Artist.id')) 