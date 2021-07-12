from django import forms
from .models import Comment, Clap

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment', 'user']

class ClapForm(forms.ModelForm):
    class Meta:
        model = Clap
        fields = ['claps_given', 'user']