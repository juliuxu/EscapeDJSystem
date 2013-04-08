from django.conf.urls import patterns, url

urlpatterns = patterns('',
	url(r'^$', 'escapedjsystem.escapedjsystem.views.home', name='home'),
    url(r'^djview', 'escapedjsystem.escapedjsystem.views.djview', name='djview'),
    url(r'^newmessage', 'escapedjsystem.escapedjsystem.views.newmessage', name='newmessage'),
    url(r'^songrequest', 'escapedjsystem.escapedjsystem.views.songrequest', name='songrequest'),

    url(r'^getmessages', 'escapedjsystem.escapedjsystem.views.getmessages', name='getmessages'),
    url(r'^getsongrequests', 'escapedjsystem.escapedjsystem.views.getsongrequests', name='getsongrequests'),


)