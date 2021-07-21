from django import forms
from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('create_time', 'blog', 'viewed')

    def send_email(self):
        pass