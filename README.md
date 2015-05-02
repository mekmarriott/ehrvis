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

1) Make sure to have latest version of pip installed. 

	IF NOT, install with:
	>> sudo easy_install pip

	For the latest version, use:
	>> sudo pip install --upgrade pip

2) Make sure to have the latest version of virtualenv installed

	>> sudo pip install virtualenv --upgrade
	# Note: This is critical for the key dependencies of Flask

2) Start a virtual environment in this directory

	>> virtualenv env 
	
	# Note: has to be named 'env' because that's in the .gitignore. Please don't name it anything else or it will be uploaded in to the git repo and no one wants that.
	
	This is how you start the virtual environment everytime you want to work in the directory. There should be a (env) by your prompt after running this command:
	>> source env/bin/activate 

	In order to get out of virtual environment after you are done working, use the following command and the '(env)' by the prompt should go away!:
	>> deactivate

3) Install all dependencies - these are outlined in requirements.txt

	>> pip install -r requirements.txt

	You can check if this successfully installed all the dependencies by comparing requirements.txt with the output of:
	>> pip freeze

4) RUN

	>> python app.py
	OR
	>> foreman start (run on web proc)
	# Note: foreman is preferred to see how it will function on the gunicorn server

5) Contributing - If you want to add python dependencies, make sure to add them to requirements.txt:

	>> pip install [my python package here]
	>> pip freeze > requirements.txt

==================================================
Specifications
==================================================

==================================================
Dependencies
==================================================
EHR Vis is built on [Flask] and HTML5.

Other dependencies include:
* [Twitter Bootstrap] - great UI boilerplate for modern web apps
* [jQuery] - duh
* [Gunicorn] - python WSGI HTTP server

==================================================
To-Dos
==================================================
- Too many to list

==================================================
License
==================================================
MIT


[Twitter Bootstrap]:http://twitter.github.com/bootstrap/
[jQuery]:http://jquery.com
[Flask]:http://flask.pocoo.org/
[Gunicorn]:http://gunicorn.org/
