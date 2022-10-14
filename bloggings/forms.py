from django import forms
from bloggings.models import Post
from bloggings.models import Comment

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'theme']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
