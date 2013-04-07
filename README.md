# Escape DJ System
Find a better name
## Description
Web application for interaction with DJ's and audience

## How to deploy

## Install requierments

	pip install Django==1.5.1
	pip install django-bootstrap-toolkit

### Create your local_settings.py

	cp local_settings_example.py local_settings.py

### Edit local_settings.py

To create a SECRET_KEY, run this in your terminal and copy the result

	< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;

### Run server

	python manage.py runserver

## Features Abstract

## Features Advanced

* User system
	- DJ
	- User
		- SSO with facebook/google/twitter
* Request a song
* Song voting
* Song poll
* Send message to DJ
* DJ Request viewer
* Next song
	- With timer, in case dj forgets to update

* Song database
	* new songs get added

* Typeahead (use song database)

* Statistics
	- Most popular song

## Technologies
* python-django
* jquery
* bootstrap front-end
* long-pooling

* Responsive design