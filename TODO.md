# TODO
* Make messages only viewable for the DJ
* Make max number of elements dynamic to fit screen
* Make into portable django app

## TODO DONE
* Make screen blink or something when a new message or song request is recived
	- Not to annoying
* Doesn't work when DEBUG = False on my production server

## Features
* Show what is currently playing (last.fm)
* Integrate twitter feed watch
	- When someone tweets "Play Gangnam style #escapeoslo", it shows up on the djview

## Bugs
* After fullscreen view on a smaller screen, the menu gets pushed down
* Very vurlnable to DoS attack
	- Send lots of POST pk=999999 to either /escaepdjsystem/getsongrequests or /escaepdjsystem/getmessages 