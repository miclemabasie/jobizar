from django import forms
from .models import Post, Comment

class EmailPostForm(forms.Form):
    name = forms.CharField(max_length=200)
    
    to_email = forms.EmailField()
    comments = forms.CharField(widget=forms.Textarea())


class CreateCommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'body']
        

class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)
    