==================================================
========= EHR VISUALIZATION PROJECT ==============
==================================================


==================================================
>> SETTING UP
==================================================

1) Make sure to have latest version of pip installed. 
! IF NOT !, install with:
	>> sudo easy_install pip

For the latest version, use:
	>> pip install --upgrade pip

2) (opt) Start a virtual environment in this directory
	>> virtualenv env 
	
	# Note: has to be named 'env' because that's in the .gitignore. Please don't name it anything else or it will be uploaded in to the git repo and no one wants that.
	
	>> source env/bin/activate 
	
	# This is how you start the virtual environment everytime you want to work in the directory. There should be a (env) by your prompt after running this command.
	>> deactivate

Note - In order to get out of virtual environment, use the following command:
	>> deactivate
	(and the '(env)' by the prompt should go away)

3) Install all dependencies - these are outlined in requirements.txt
	>> pip install -r requirements.txt
	# This might take a while...

	# You can check if this successfully installed all the dependencies by comparing requirements.txt with the output of:
	>> pip freeze

4) RUN
	>> python app.py
	OR
	>> foreman start (run on web proc)
	# foreman is preferred to see how it will function on a larger server (i.e. gunicorn)

==================================================
>> ADD README + SPECS HERE !!!!!!
==================================================

