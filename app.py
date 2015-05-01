"""
References:

Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

"""

import os
from flask import Flask, render_template, request, redirect, url_for
# from waitress import serve

#=======================================================================
#       Application Configuration
#=======================================================================
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'EHR_visualization_2015') #<= not-so-secret key for now
#=======================================================================

#=======================================================================
#       General routing for application
#=======================================================================
@app.route('/')
def home():
    """Render website's home page."""
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')
#=======================================================================

#=======================================================================
#       Routing for all AJAX calls
#=======================================================================
@app.route('/_notes/')
def notes():
    """Return all patient note information."""
    return None

@app.route('/_medications/')
def medications():
    """Return all medication information."""
    return None
#=======================================================================


########################################################################
#       Maintenance functions for Flask apps.
#=======================================================================
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=600'
    return response

@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404
#=======================================================================


#=======================================================================
#       RUN APPLICATION!
#=======================================================================
if __name__ == '__main__':
    app.run(debug=True)
    # serve(app)
#=======================================================================