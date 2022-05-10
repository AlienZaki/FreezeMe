from django import forms



class submissionForm(forms.Form):
    hidden = forms.HiddenInput()
    FINISHED_CHOICES = [
        (True, 'Finished'),
        (False, 'Processing')
    ]
    #finished = forms.ChoiceField(choices=FINISHED_CHOICES, label="Some Label", initial='', widget=forms.Select(), required=True)


class settingsForm(forms.Form):
    hidden = forms.HiddenInput()


class clientForm(forms.Form):
    hidden = forms.HiddenInput()
