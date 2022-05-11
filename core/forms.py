from django import forms
from .models import Client, Settings



class submissionForm(forms.Form):
    hidden = forms.HiddenInput()
    FINISHED_CHOICES = [
        (True, 'Finished'),
        (False, 'Processing')
    ]
    #finished = forms.ChoiceField(choices=FINISHED_CHOICES, label="Some Label", initial='', widget=forms.Select(), required=True)



class settingsForm(forms.ModelForm):
    class Meta:
        model = Settings
        fields = '__all__'


class clientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
