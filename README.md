<!-- Author: Emma Marriott -->


==================================================
>> EHR VISUALIZATION PROJECT 
==================================================

==================================================
Description
==================================================
EHR Vis is a simple web application demo that visualizes electronic health record data in an intuitive way. It utilizes FHIR REST frameworks and HL7 models to integrate with any FHIR server (demo uses EPIC sandbox). See the application live at https://ehrvis.herokuapp.com/

==================================================
Setting Up
==================================================

1) Install the heroku tool belt here: https://toolbelt.heroku.com/

2) Make sure you have latest version of pip installed. 

	If you don't have pip, install with:
	>> sudo easy_install pip

	To upgrade to the latest version of pip, use:
	>> sudo pip install --upgrade pip

3) Make sure to have the latest version of virtualenv installed

	>> sudo pip install virtualenv --upgrade
	# Note: This is critical for the key dependencies of Flask

4) Start a virtual environment in this directory

	>> virtualenv env 
	
	# Note: has to be named 'env' because that's in the .gitignore. Please don't name it anything else or it will be uploaded in to the git repo and no one wants that.
	
	This is how you start the virtual environment everytime you want to work in the directory. There should be a (env) by your prompt after running this command:
	>> source env/bin/activate 

	In order to get out of virtual environment after you are done working, use the following command and the '(env)' by the prompt should go away!:
	>> deactivate

5) Install all dependencies - these are outlined in requirements.txt

	>> pip install -r requirements.txt

	You can check if this successfully installed all the dependencies by comparing requirements.txt with the output of:
	>> pip freeze

6) Running - go to localhost://5000 on your browser to see the application after running the following commands

	>> python app.py
	OR (if you want to use a real web server)
	>> foreman start (run on web proc)

7) Contributing - If you want to add python dependencies, make sure to add them to requirements.txt:

	>> pip install [my python package here]
	>> pip freeze > requirements.txt

==================================================
Specifications
==================================================
Just to make organization easier, I'm going to list the files and what should go in these files:
- **static/css:** All the css (styling) files for the web application. Add any other template pages you want but do not modify any page except *style.css*
- **static/css/style.css:** This is where you can add your styling changes. Since it is the last file included, it will take precedence over ther template css files mentioned above
- **static/fonts:** Not really important, unless you find a font you absolutely must have in which case put it in this folder
- **static/js:** All the standard javascripts we want to include. You can add more standard javascripts to this file, but don't modify any of them
- **static/scripts:** All of our javascripts. This includes *Medication.js* for the Medication javascript class, *Note.js* for the Note javascript class, and *dashboard.js* for any other external functions we might need
- **robots.txt:** Not important, don't worry about it (it's for search stuff)
- **Makefile, Procfile:** Don't change please this is for the Heroku/other configuration
- **.gitignore:** Has pretty much everything covered so you can ignore it
- **requirements.txt:** Change when you install a new python dependency (as described in step 7 of Setting Up)
- **app.py:** Where all the magic happens
- **medications.py:** For python data models related to medications
- **notes.py:** For python data models related to clinical notes

==================================================
Dependencies
==================================================
EHR Vis is built on [Flask] and HTML5.
Other dependencies include:
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [jQuery] - duh
* [Gunicorn] - python WSGI HTTP server


==================================================
License
==================================================
MIT

[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[jQuery]:http://jquery.com
[Flask]:http://flask.pocoo.org/
[Gunicorn]:http://gunicorn.org/
