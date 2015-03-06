    # Roadi
    # Copyright (C) 2014 Jake Nyquist, Philip Taffet, Brett Gutstein

    # This program is free software; you can redistribute it and/or modify
    # it under the terms of the GNU General Public License as published by
    # the Free Software Foundation; either version 2 of the License, or
    # (at your option) any later version.

    # This program is distributed in the hope that it will be useful,
    # but WITHOUT ANY WARRANTY; without even the implied warranty of
    # MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    # GNU General Public License for more details.

    # You should have received a copy of the GNU General Public License along
    # with this program; if not, write to the Free Software Foundation, Inc.,
    # 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
    
    # To contact the authors, write us at nyquist11 (at) gmail (dot) com

"""
Routes and views for the flask application.
"""

from datetime import datetime, timedelta
from flask import render_template
from FlaskWebProject import app
from flask import stream_with_context, request, Response
import time
import process_query
from location_list import get_location
import dateutil.parser
import process_query
import airports
from urllib import urlencode

@app.route('/')
def home():
    """Renders the home page."""
    return render_template('index.html',
        title='Home',
        year=datetime.now().year,)

@app.route("/results")
def results():
    data = process_query.process_query(request.args["q"], request.args["s"], request.args["e"], request.args["c"], int(request.args["p"]))
    return render_template('results.html', results = data)

@app.route("/search", methods=["POST"])
def search():

   startDateTime = dateutil.parser.parse(request.form['startDateTime'])
   endDateTime = dateutil.parser.parse(request.form['endDateTime']) + timedelta(1)
   rqparams = {"q": request.form['entity'], 
               "s": startDateTime.strftime("%Y-%m-%dT%H:%M"),
               "e": endDateTime.strftime("%Y-%m-%dT%H:%M"),
               "c": airports.airports(request.form['startingCity'])}

   return render_template('results-loading.html', title='Results', year=datetime.now().year, querystring=urlencode(rqparams))


@app.route("/autosearch", methods=["GET"])
def defaultsearch():
    startDateTime = datetime.today()
    endDateTime = datetime.today() + timedelta(365)
    try:
        startingCity = get_location(request.remote_addr)
    except:
        startingCity = "Dallas"
    startingCity = airports.airports(startingCity)

    entity = request.args["q"]
    rqparams = {"q": entity, 
                "s": startDateTime.strftime("%Y-%m-%dT%H:%M"),
                "e": endDateTime.strftime("%Y-%m-%dT%H:%M"),
                "c": startingCity}

    return render_template('results-loading.html', title='Results', querystring = urlencode(rqparams), year=datetime.now().year)



@app.route('/about')
def about():
    """Renders the about page."""
    return render_template('about.html',
        title='About',
        year=datetime.now().year,)

@app.route('/advanced')
def advanced():
    """Renders the advanced search page."""
    return render_template('advanced.html',
        title='Advanced Search',
        year=datetime.now().year
    )

