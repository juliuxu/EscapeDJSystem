from django import forms
from models import *


class NewMessageForm(forms.ModelForm):

    class Meta:
        model = Message
        fields = ('text',)

    def __init__(self, *args, **kwargs):
        super(NewMessageForm, self).__init__(*args, **kwargs)
        self.fields['text'].label = ''
        self.fields['text'].widget.attrs.update({
            'placeholder': 'Ex: Turn up the volume!',
            'class': 'input-block-level'
        })


class SongRequestForm(forms.Form):
    song = forms.CharField()

    def __init__(self, *args, **kwargs):
        super(SongRequestForm, self).__init__(*args, **kwargs)
        self.fields['song'].label = ''
        self.fields['song'].max_length = 100
        self.fields['song'].widget.attrs.update({
            'autocomplete': 'off',
            'placeholder': 'Ex: Numb/Encore by Linkin Park and Jay-Z',
            'class': 'input-block-level'
        })
