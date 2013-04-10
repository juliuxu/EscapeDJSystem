# Escape DJ System

Web application for interaction between a DJ and an audience

## How to deploy

### Install requierments

	pip install Django==1.5.1
	pip install flup
	pip install django-bootstrap-toolkit

### Create your local_settings.py

	cp local_settings_example.py local_settings.py

### Edit local_settings.py

To create a SECRET_KEY, run this in your terminal and copy the result

	< /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c${1:-32};echo;

### Set up nginx

Create a new site

	touch /etc/nginx/sites-available/escapedjsystem
	ln /etc/nginx/sites-available/escapedjsystem /etc/nginx/sites-enabled/escapedjsystem -s

And paste into this configuration, and change it.

	server {

	    server_name dj.escapeoslo.net;

	    access_log /var/log/nginx/escapedjsystem.access.log;
	    error_log /var/log/nginx/escapedjsystem.error.log;
	    
	    location /media/ { # MEDIA_URL
	        alias /home/escapedjsystem/EscapeDJSystem/escapedjsystem/media/;
	        expires 30d;
	    }

	    location / {
	        fastcgi_split_path_info ^()(.*)$;
                fastcgi_read_timeout 120;
	        include fastcgi_params;
	        fastcgi_pass 127.0.0.1:40001;
	    }
	}


### Run server

For developing:

	python manage.py runserver

With fastcgi, use the start_stop.sh script

	sh start_stop.sh start

### Set up monitor

Set your monitorscreen to go to

	http://yoururl.com/djview#fullscreenmonitor

## Features Implemented
* DJ View
	- Panel for DJ to keep track of requests and messages
* Sending messages to the DJ
* Requesting songs
* Simple song database
	- Gets populated by requests
* Typeahead on song request

## Features Todo

* User system
	- DJ
	- User
		- SSO with facebook/google/twitter
* Song voting
	- Vote on requested songs
* Song poll
	- Vote on a list of songs
* Next song
	- With timer, in case dj forgets to update
* Statistics
	- Most popular song

## Technologies
* python-django
* jquery
* bootstrap front-end
* long-pooling
