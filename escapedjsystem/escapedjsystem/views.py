from django.http import HttpResponse, HttpResponseBadRequest
from django.template import RequestContext
from django.shortcuts import render_to_response
from models import Message, Song, SongRequest
from forms import NewMessageForm, SongRequestForm

from datetime import timedelta
import simplejson
from time import sleep

from django.utils.timezone import localtime, now

from django.db import transaction
from django.conf import settings

#############################################################


@transaction.commit_manually
def flush_transaction():
    """
    Flush the current transaction so we don't read stale data

    Use in long running processes to make sure fresh data is read from
    the database.  This is a problem with MySQL and the default
    transaction mode.  You can fix it by setting
    "transaction-isolation = READ-COMMITTED" in my.cnf or by calling
    this function at the appropriate moment
    """
    transaction.commit()


def alerthtml(alertype, title, message):
    return """<div class="alert %s fade">
          <button type="button" class="close" data-dismiss="alert">&times;</button>
      <strong>%s</strong> %s
    </div><script>$('.alert').closest('.alert').fadeIn(1).addClass('in')</script>""" % (alertype, title, message)
    #Todo: improve (make code prettier) javascript fadein


def render_helper(template, c, request):

    c['bootstrap_style'] = settings.BOOTSTRAP_STYLE

    return render_to_response(template, RequestContext(request, c))

####################################################################


def home(request):
    c = {}
    c['title'] = 'Escape DJ System'

    c['songrequests'] = SongRequest.objects.order_by('-pk')[:5]
    c['newMessageForm'] = NewMessageForm()
    c['songRequestForm'] = SongRequestForm()

    #Previous songs for typeahead
    c['songs'] = Song.objects.order_by('-date')[:500]

    return render_helper('esc_home.html', c, request)


def djview(request):
    c = {}
    c['title'] = 'Escape DJ View'

    c['msgs'] = Message.objects.order_by('-pk')[:7]
    c['songrequests'] = SongRequest.objects.order_by('-pk')[:7]

    # c['bootstrap_style'] = 'slate'

    if request.method == "GET" and 'fullscreen' in request.GET:
        c['fullscreen'] = True

    request.META["CSRF_COOKIE_USED"] = True

    return render_helper('esc_djview.html', c, request)


def about(request):
    c = {}
    c['title'] = ''

    return render_helper('esc_about.html', c, request)


def newmessage(request):

    c = {}

    if request.method == 'POST':
        newMessageForm = NewMessageForm(request.POST)
        if newMessageForm.is_valid():
            newMessageForm.save()
            response = alerthtml('alert-success', 'Success!', 'Your message was sent to the DJ')
        else:
            response = alerthtml('alert-error', 'Error!', 'Please fill in all fields!')

        if request.is_ajax():
            return HttpResponse(simplejson.dumps({'html': response}), content_type="application/json")
        else:
            c['form_result'] = response

    c['title'] = 'Send a message to the DJ'

    c['newMessageForm'] = NewMessageForm()
    return render_helper('esc_newmessage.html', c, request)


def songrequest(request):

    c = {}
    c['title'] = 'Request a song'

    if request.method == 'POST':
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

        if request.is_ajax():
            return HttpResponse(simplejson.dumps({'html': response}), content_type="application/json")
        else:
            c['form_result'] = response

    c['songRequestForm'] = SongRequestForm()

    #Previous songs for typeahead
    c['songs'] = Song.objects.order_by('-date')[:500]

    return render_helper('esc_songrequest.html', c, request)


def getmessages(request):

    if not request.method == "POST":
        return HttpResponseBadRequest()

    if 'pk' not in request.POST:
        return HttpResponseBadRequest()

    pk = request.POST['pk']
    for _ in xrange(20):
        messages = Message.objects.filter(pk__gt=pk).order_by('pk')[:100]
        flush_transaction()
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
        flush_transaction()
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
