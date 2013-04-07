from django import forms
from models import Message

class NewMessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ('text',)

class SongRequestForm(forms.Form):
    song = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'autocomplete':'off', 'data-provide':'typeahead'}))