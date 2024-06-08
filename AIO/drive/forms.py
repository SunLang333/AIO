from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()
    path = forms.CharField(widget=forms.HiddenInput(), required=False)
