# TODO: formatting notes/get better notes
# TODO: get better med list?
# TODO: replace toastr with polymer toast
# TODO: organize medications by name
# TODO: get medication groupings (snomed code?)



"""
References:

Flask Documentation:     http://flask.pocoo.org/docs/
Jinja2 Documentation:    http://jinja.pocoo.org/2/documentation/
Werkzeug Documentation:  http://werkzeug.pocoo.org/documentation/

"""

import os
from flask import Flask, render_template, request, redirect, url_for, jsonify
from medications import load_patient1_meds
from notes import load_epic_notes, date2utc
from time import mktime
import json

global medication_data
global note_data

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
    print "RENDERING HOME.HTML"
    return render_template('home.html')


@app.route('/about/')
def about():
    """Render the website's about page."""
    return render_template('about.html')

@app.route('/timeline/')
def timeline():
    """Render prototype of timeline"""
    return render_template('timeline.html')

@app.route('/flot/')
def flot():
    """Render prototype of timeline"""
    return render_template('flot.html')
#=======================================================================

#=======================================================================
#       Routing for all AJAX calls
#=======================================================================
@app.route('/_medications/')
def medications():
    global medication_data
    print "Called"
    """Return all medication information."""
    medication_data = load_patient1_meds()
    print medication_data.medNames
    return jsonify(medication_data=medication_data.meds, 
                            minDate=medication_data.minDate,
                            med_indices=[k for k in medication_data.idx2med],
                            med_names=[medication_data.idx2med[k] for k in medication_data.idx2med])

@app.route('/_notes/')
def notes():
    global note_data
    print "Called"
    """Return all note information."""
    # note_data = load_mimic_notes()
    note_data = load_epic_notes()
    return jsonify(previewData=note_data.previewsByService, plottingSeries=note_data.series.values(), 
                    hospitalizations=note_data.hospitalizations, minDate=date2utc(note_data.minDate), maxDate=date2utc(note_data.maxDate))


@app.route('/_note/<service_id>/<note_id>/fulltext/')
def note_fulltext(service_id,note_id):
    global note_data
    i=int(note_id)
    print "Fulltext requested"
    # print note_data.notes[t]
    try:
        return jsonify(fulltext=note_data.notesByService[service_id][i].fulltext)
    except:
        return jsonify(fulltext="Unavailable")

@app.route('/_note/<service_id>/<note_id>/preview/')
def note_preview(sevice_id,note_id):
    global note_data
    i=int(note_id)
    print "Preview requested"
    # print note_data.notes[t]
    try:
        return jsonify(fulltext=note_data.notesByService[service_id][i].preview)
    except:
        return jsonify(fulltext="Unavailable")

@app.route('/_nulltest/')
def nulltest():
    return jsonify(retval = [[1,3],[2,4],None,[3,3]])

#=======================================================================


#=======================================================================
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
#=======================================================================