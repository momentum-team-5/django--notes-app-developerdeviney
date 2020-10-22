from django import forms
from .models import Note


class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = [
            'title',
            'body'
        ]

class ContactForm(forms.Form):
    email = forms.EmailField(required=True)
    title = forms.CharField(max_length=255, required=True)
    body = forms.CharField(label="Type your message", max_length=255, widget=forms.Textarea(attrs={'required':True}))

class SearchForm(forms.Form):
    title = forms.CharField(required=True, max_length=255)
    order_by = forms.ChoiceField(choices=[("title", "title"), ("body", "body")])


