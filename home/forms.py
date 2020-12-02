from django import forms


def should_be_empty(value):
    if value:
        raise forms.ValidationError("Field is not empty")

class ContactForm(forms.Form):
    name = forms.CharField(max_length=60, label="Name", 
                            required=True)
    subject = forms.CharField(max_length=120, 
                            label="Subject", required=True)
    sender = forms.EmailField(label="Email", required=True)
    message = forms.CharField(widget=forms.Textarea, 
                            label="Message", required=True)
    forcefield = forms.CharField(required=False, 
                            widget=forms.HiddenInput, 
                            label="Leave empty", 
                            validators=[should_be_empty])