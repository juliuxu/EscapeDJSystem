from django.http import HttpResponse
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Message, Song, SongRequest
from forms import NewMessageForm, SongRequestForm

from bootstrap_toolkit.widgets import BootstrapUneditableInput

from datetime import datetime, timedelta

def home(request):
	c = {}
	c['title'] = 'Escape DJ System'

	return render_to_response('esc_home.html', RequestContext(request,c))

def djview(request):
	c = {}
	c['title'] = 'Escape DJ View'

	c['msgs'] = Message.objects.order_by('-date')[:5]
	c['songrequests'] = SongRequest.objects.order_by('-date')[:5]

	return render_to_response('esc_djview.html', RequestContext(request,c))

def newmessage(request):
	c = {}
	c['title'] = 'Send a message to the DJ'

	if request.method == 'POST':
		newMessageForm = NewMessageForm(request.POST)
		if newMessageForm.is_valid():
			newMessageForm.save()
			c['success'] = True
		else:
			c['failure'] = "Form not valid"
	else:
		newMessageForm = NewMessageForm()

	c['newMessageForm'] = newMessageForm

	return render_to_response('esc_newmessage.html', RequestContext(request,c))

def songrequest(request):
	c = {}
	c['title'] = 'Request a song'

	if request.method == 'POST':
		songRequestForm = SongRequestForm(request.POST)
		if songRequestForm.is_valid():
			try:
				song = Song.objects.get(text=songRequestForm.cleaned_data['song'])
			except Song.DoesNotExist:
				song = Song(text=songRequestForm.cleaned_data['song'])
				song.save()

			#Check if same song has been requested in the last 15 min
			lastSongRequests = SongRequest.objects.filter(date__gte=(datetime.today() - timedelta(minutes=15)) )
			for x in lastSongRequests:
				if x.song == song:
					c['failure'] = "That song has already been requested in the last 15 minutes"
					break
			else:
				songRequest = SongRequest(song=song)
				songRequest.save()
				c['success'] = True
		else:
			c['failure'] = "Form not valid"
	else:
		songRequestForm = SongRequestForm()

	c['songRequestForm'] = songRequestForm

	#Previous songs for typeahead
	c['songs'] = Song.objects.order_by('-date')[:500]

	return render_to_response('esc_songrequest.html', RequestContext(request,c))