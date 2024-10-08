#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_migrate import Migrate
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from sqlalchemy import Column, ARRAY, ForeignKey, Integer, String, func
from models import Artist, Shows, Venue, db
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
db.init_app(app)
migrate = Migrate(app, db)

# TODO: connect to a local postgresql database - done  

    # TODO: implement any missing fields, as a database migration using Flask-Migrate - done


# TODO Implement Show and Artist models, and complete all model relationships and properties, as a database migration. - done

with app.app_context():
    db.create_all()

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  if isinstance(value, str):
        date = dateutil.parser.parse(value)
  else:
        date = value
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  # TODO: replace with real venues_arr data - done
  #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue. - done

    areas = []
    venues = Venue.query.all()
    places = Venue.query.distinct(Venue.city, Venue.state).order_by(Venue.city.desc(), Venue.state.desc()).all()
    for place in places:
        tmp_venues = []
        for venue in venues:
            if venue.city == place.city and venue.state == place.state:
                num_shows = 0
                print('shows - ')
                print(venue.shows)
                for show in venue.shows:
                    if show.start_time > datetime.now():
                        num_shows += 1
                    tmp_venues.append(
                            {
                              'id': venue.id,
                              'name': venue.name,
                              'num_upcoming_shows': num_shows
                            }
                              
                      )
        areas.append({
            'city': place.city,
            'state': place.state,
            'venues': tmp_venues
        })
        print('areas - ')
        print(areas)
    return render_template('pages/venues.html', areas=areas)

@app.route('/venues/search', methods=['POST'])
def search_venues():
  # TODO: implement search on venues_arr with partial string search. Ensure it is case-insensitive. - done
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  search_term = request.form.get('search_term')
  venues = Venue.query.filter_by(Venue.name.contains(search_term)).all()
  num_shows = 0
  for venue in venues:
    for show in venue.shows:
                      if show.start_time > datetime.now():
                          num_shows += 1
  response = venues
  response={
    "count": len(venues),
    "data": venues,
    "num_upcoming_shows": num_shows
  }
  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  # TODO: replace with real venue data from the venues_arr table, using venue_id - done
  venues = Venue.query.filter_by(id=venue_id).one_or_none()
  data = venues
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  # TODO: insert form data as a new Venue record in the db, instead - done
  # TODO: modify data to be the data object returned from db insertion - done

    # Set the FlaskForm
    form = VenueForm(request.form, meta={"csrf": False})
# Validate all fields
    if form.validate():
    # Prepare for transaction
        try:
                venue = Venue(
                name=form.name.data,  # The correct way...
                city = form.city.data,
                state = form.state.data,
                address = form.address.data,
                phone = form.phone.data,
                genres = form.genres.data,
                facebook_link = form.facebook_link.data,
                website = form.website_link.data,
                image_link = form.image_link.data,
                seeking_talent = form.seeking_talent.data,
                seeking_description = form.seeking_description.data
            )
                db.session.add(venue)
                db.session.commit()
        except ValueError as e:
            print(e)
        # If there is any error, roll back it
            db.session.rollback()
        finally:
            db.session.close()
        flash("Venue " + request.form["name"] + " was successfully listed!")
        return render_template("pages/home.html")
# If there is any invalid field
    else:
        message = []
        for field, errors in form.errors.items():
            for error in errors:
                message.append(f"{field}: {error}")
        flash("Please fix the following errors: " + ", ".join(message))
        form = VenueForm()
        return render_template("forms/new_venue.html", form=form)


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
  # TODO: Complete this endpoint for taking a venue_id, and using - done
  # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail. - done
    venue = Venue.session.query(Venue.id == venue_id)
    db.session.delete(venue)
    try:
        db.session.commit()
    except:
        db.session.rollback()
  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
    return None

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  # TODO: replace with real data returned from querying the database - done
  artists = Artist.query.all()
  data = artists
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():
  # TODO: implement search on artists with partial string search. Ensure it is case-insensitive. - done
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  artists = Artist.query.filter_by(Artist.name.contains(search_term)).all()
  num_shows = 0
  for artist in artists:
    for show in artist.shows:
                      if show.start_time > datetime.now():
                          num_shows += 1
  response={
    "count": len(artists),
    "data": artists,
    "num_upcoming_shows": num_shows
  }
  # response={
  #   "count": 1,
  #   "data": [{
  #     "id": 4,
  #     "name": "Guns N Petals",
  #     "num_upcoming_shows": 0,
  #   }]
  # }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  # shows the artist page with the given artist_id
  # TODO: replace with real artist data from the artist table, using artist_id - done
  artists = Artist.query.filter_by(id=artist_id).all()
  data = artists
  if(len(data) > 0):
    print(data)
    return render_template('pages/show_artist.html', artist=data[0])

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm(request.form, meta={"csrf": False})
  artists = Artist.query.filter_by(id=artist_id).all()
  print(artists)
  if(len(artists) > 0):
    artist={
      "id": artists[0].id,
      "name": artists[0].name,
      "genres": artists[0].genres,
      "city": artists[0].city,
      "state": artists[0].state,
      "phone": artists[0].phone,
      "website": artists[0].website,
      "facebook_link": artists[0].facebook_link,
      "seeking_venue": artists[0].seeking_venue,
      "seeking_description": artists[0].seeking_description,
      "image_link": artists[0].image_link
    }
  # TODO: populate form with fields from artist with ID <artist_id> - done
  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  # TODO: take values from the form submitted, and update existing - done
  # artist record with ID <artist_id> using the new attributes
  form = ArtistForm(request.form, meta={"csrf": False})
  artist = Artist.query(Artist.id == artist_id).one_or_none()
  artist.name = form.name.data
  artist.genres = form.genres.data
  artist.city = form.city.data
  artist.state = form.state.data
  artist.phone = form.phone.data
  artist.website = form.website.data
  artist.facebook_link = form.facebook_link.data
  artist.image_link = form.image_link.data
  artist.seeking_talent = form.seeking_talent.data
  artist.seeking_description = form.seeking_description.data
  db.session.add(artist)
  db.session.commmit()
  return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm(request.form, meta={"csrf": False})
  v = db.session.query(Venue).filter_by(id=venue_id).one_or_none()
  venue={
    "id": v.id,
    "name": v.name,
    "genres": v.genres,
    "address": v.address,
    "city": v.city,
    "state": v.state,
    "phone": v.phone,
    "website": v.website,
    "facebook_link": v.facebook_link,
    "seeking_talent": v.seeking_talent,
    "seeking_description": v.seeking_description,
    "image_link": v.image_link
  }
  # TODO: populate form with values from venue with ID <venue_id> - done
  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  # TODO: take values from the form submitted, and update existing - done
  # venue record with ID <venue_id> using the new attributes
    form = VenueForm(request.form, meta={"csrf": False})
    venue = Venue.query(Venue.id == venue_id).one_or_none()
    venue.name=form.name.data,  # The correct way...
    venue.city = form.city.data,
    venue.state = form.state.data,
    venue.address = form.address.data,
    venue.phone = form.phone.data,
    venue.genres = form.genres.data,
    venue.facebook_link = form.facebook_link.data,
    venue.website = form.website_link.data,
    venue.image_link = form.image_link.data,
    venue.seeking_talent = form.seeking_talent.data,
    venue.seeking_description = form.seeking_description.data
    try:
        db.session.add(venue)
        db.session.commit()
  # on successful db insert, flash success
        flash('Venue ' + request.form['name'] + ' was successfully updated!')
  # TODO: on unsuccessful db insert, flash an error instead. - done
    except:
        db.session.rollback()
        flash('An error occurred. Venue ' + venue.name + ' could not be updated.')
    return redirect(url_for('show_venue', venue_id=venue_id))

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # TODO: insert form data as a new Venue record in the db, instead - done
  # TODO: modify data to be the data object returned from db insertion - done

    form = ArtistForm(request.form, meta={"csrf": False})
    artist = Artist()
    artist.name = form.name.data
    artist.genres = form.genres.data
    artist.city = form.city.data
    artist.state = form.state.data
    artist.phone = form.phone.data
    artist.website = form.website.data
    artist.facebook_link = form.facebook_link.data
    artist.image_link = form.image_link.data
    artist.seeking_talent = form.seeking_talent.data
    artist.seeking_description = form.seeking_description.data
    db.session.add(artist)
    db.session.commmit()
    try:
      db.session.commit()
  # on successful db insert, flash success
      flash('Artist ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
    except:
      flash('An error occurred. Artist ' + artist.name + ' could not be listed.')
    return render_template('pages/home.html')


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  # TODO: replace with real venues data. - done
  shows = Shows.query.all()
  data = shows
  print(shows)
  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # TODO: insert form data as a new Show record in the db, instead - done
    form =ShowForm(request.form, meta={"csrf": False})
  # on successful db insert, flash success
    show = Shows()
    show.start_time = form.start_time.data
    show.artist_id = form.artist_id.data
    show.venue_id = form.venue_id.data
    db.session.add(show)
    try:
      db.session.commit()
  # on successful db insert, flash success
    # flash('Venue ' + request.form['name'] + ' was successfully listed!')
      flash('Show was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead. - done
    except:
        flash('An error occurred. Show could not be listed.')
  # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
