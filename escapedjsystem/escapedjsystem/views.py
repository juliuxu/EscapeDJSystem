from django.http import HttpResponse, HttpResponseBadRequest
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Message, Song, SongRequest
from forms import NewMessageForm, SongRequestForm

from datetime import timedelta
import simplejson
from time import sleep

from django.utils.timezone import localtime, now


def alerthtml(alertype, title, message):
    return """<div class="alert %s fade">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
      <strong>%s</strong> %s
    </div><script>$('.alert').closest('.alert').fadeIn(1).addClass('in')</script>""" % (alertype, title, message)
    #Todo: improve (make code prettier) javascript fadein


def home(request):
    c = {}
    c['title'] = 'Escape DJ System'

    return render_to_response('esc_home.html', RequestContext(request, c))


def djview(request):
    c = {}
    c['title'] = 'Escape DJ View'

    c['msgs'] = Message.objects.order_by('-pk')[:5]
    c['songrequests'] = SongRequest.objects.order_by('-pk')[:5]

    if request.method == "GET" and 'fullscreen' in request.GET:
        c['fullscreen'] = True

    return render_to_response('esc_djview.html', RequestContext(request, c))


def about(request):
    c = {}
    c['title'] = ''

    return render_to_response('esc_about.html', RequestContext(request, c))


def newmessage(request):
    if request.method == 'POST' and request.is_ajax():
        newMessageForm = NewMessageForm(request.POST)
        if newMessageForm.is_valid():
            newMessageForm.save()
            response = alerthtml('alert-success', 'Success!', 'Your message was added to the DJ queue')
        else:
            response = alerthtml('alert-error', 'Error!', 'Please fill in all fields!')

        return HttpResponse(simplejson.dumps({'html': response}), content_type="application/json")

    else:
        c = {}
        c['title'] = 'Send a message to the DJ'

        newMessageForm = NewMessageForm()
        c['newMessageForm'] = newMessageForm
        return render_to_response('esc_newmessage.html', RequestContext(request, c))


def songrequest(request):

    c = {}
    c['title'] = 'Request a song'

    if request.method == 'POST' and request.is_ajax():
        songRequestForm = SongRequestForm(request.POST)
        response = ''
        if songRequestForm.is_valid():
            try:
                song = Song.objects.get(text=songRequestForm.cleaned_data['song'])
            except Song.DoesNotExist:
                song = Song(text=songRequestForm.cleaned_data['song'])
                song.save()

            #Check if same song has been requested in the last 15 min
            lastSongRequests = SongRequest.objects.filter(date__gte=(now() - timedelta(minutes=15)))

            for x in lastSongRequests:
                if x.song == song:
                    response = alerthtml('alert-error', 'Error!', 'That song has already been requested in the last 15 minutes')
                    break
            else:
                songRequest = SongRequest(song=song)
                songRequest.save()
                response = alerthtml('alert-success', 'Success!', 'Your song has been requested')

        else:
            response = alerthtml('alert-error', 'Error!', 'Please fill in all fields!')

        return HttpResponse(simplejson.dumps({'html': response}), content_type="application/json")

    else:
        songRequestForm = SongRequestForm()

        c['songRequestForm'] = songRequestForm

        #Previous songs for typeahead
        c['songs'] = Song.objects.order_by('-date')[:500]

        return render_to_response('esc_songrequest.html', RequestContext(request, c))


def getmessages(request):

    if not request.method == "POST":
        return HttpResponseBadRequest()

    if 'pk' not in request.POST:
        return HttpResponseBadRequest()

    pk = request.POST['pk']
    for _ in xrange(20):
        messages = Message.objects.filter(pk__gt=pk).order_by('pk')[:100]
        if messages:
            jmessages = []
            for x in messages:
                jmessages.append(
                    {
                        'pk': x.pk,
                        'text': x.text,
                        'seen': x.seen,
                        'date': localtime(x.date).strftime("%c")
                    }
                )
            return HttpResponse(simplejson.dumps(jmessages), content_type="application/json")

        sleep(1)

    return HttpResponse('OK')


def getsongrequests(request):
    if not request.method == "POST":
        return HttpResponseBadRequest()

    if 'pk' not in request.POST:
        return HttpResponseBadRequest()

    pk = request.POST['pk']
    for _ in xrange(60):
        songs = SongRequest.objects.filter(pk__gt=pk).order_by('pk')[:100]
        if songs:
            jsongs = []
            for x in songs:
                jsongs.append(
                    {
                        'pk': x.pk,
                        'text': x.song.text,
                        'played': x.played,
                        'date': localtime(x.date).strftime("%c")
                    }
                )
            return HttpResponse(simplejson.dumps(jsongs), content_type="application/json")

        sleep(1)

    return HttpResponse('OK')
