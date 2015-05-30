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
from medications import load_patient1_meds, load_playground_meds
from notes import load_epic_notes, load_playground_notes
from ehrvisutil import date2utc
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
def about():
    """Render website's home page."""
    print "RENDERING HOME.HTML"
    return render_template('about.html')


# @app.route('/dashboard/')
# def dashboard():
#     """Render the website's about page."""
#     return render_template('home.html')

@app.route('/notes_demo/')
def note_timeline():
    """Render prototype of timeline"""
    return render_template('notes_demo.html')

@app.route('/meds_demo/')
def med_timeline():
    """Render prototype of timeline"""
    return render_template('meds_demo.html')  

@app.route('/notes_eval/')
def note_eval():
    """Render prototype of timeline"""
    return render_template('notes_eval.html')

@app.route('/meds_eval/')
def med_eval():
    """Render prototype of timeline"""
    return render_template('meds_eval.html')  

#=======================================================================

#=======================================================================
#       Routing for all AJAX calls
#=======================================================================
@app.route('/_medications/')
@app.route('/_medications/<case_id>')
def medications(case_id=None):
    global medication_data
    print "Called med data load"
    """Return all medication information."""
    if case_id == "playground":
        medication_data = load_playground_meds()
    else:
        medication_data = load_patient1_meds()
    return jsonify(medication_data=medication_data)

@app.route('/_notes/')
@app.route('/_notes/<case_id>')
def notes(case_id=None):
    global note_data
    print "Called"
    """Return all note information."""
    if case_id == "playground":
        note_data = load_playground_notes()
    else:
        note_data = load_epic_notes()    
        print note_data
    return jsonify(previewData=note_data.previewsByService, plottingSeries=note_data.series.values(), 
                    hospitalizations=note_data.hospitalizations, minDate=date2utc(note_data.minDate), maxDate=date2utc(note_data.maxDate))


@app.route('/_services/')
def services():
    global note_data
    try:
        return jsonify(services=note_data.notesByService.keys())
    except:
        return jsonify(services="Unavailable")

@app.route('/_note/<service_id>/<note_id>/fulltext/')
def note_fulltext(service_id,note_id):
    global note_data
    i=int(note_id)
    print "Fulltext requested"
    return jsonify(fulltext=note_data.notesByService[service_id][i].fulltext)
    # try:
    #     print note_data.notesByService[service_id][i].fulltext
    #     return jsonify(fulltext=note_data.notesByService[service_id][i].fulltext)
    # except:
    #     return jsonify(fulltext="Unavailable")

@app.route('/_note/<service_id>/<note_id>/preview/')
def note_preview(sevice_id,note_id):
    global note_data
    i=int(note_id)
    print "Preview requested"
    try:
        return jsonify(fulltext=note_data.notesByService[service_id][i].preview)
    except:
        return jsonify(fulltext="Unavailable")



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