from django import forms


class UrlForm(forms.Form):
    your_url = forms.CharField(label='Your name', max_length=100)
