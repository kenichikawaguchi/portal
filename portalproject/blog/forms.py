from django import forms
from .models import BlogPost


class ContactForm(forms.Form):
    name = forms.CharField(label="Name")
    email = forms.EmailField(label="Email")
    title = forms.CharField(label="Title")
    message = forms.CharField(label="Message", widget=forms.Textarea)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder']\
            = "Please input your name."
        self.fields['name'].widget.attrs['class'] = 'form-control'

        self.fields['email'].widget.attrs['placeholder']\
            = "Please input your email."
        self.fields['email'].widget.attrs['class'] = 'form-control'

        self.fields['title'].widget.attrs['placeholder']\
            = "Please input title."
        self.fields['title'].widget.attrs['class'] = 'form-control'

        self.fields['message'].widget.attrs['placeholder']\
            = "Please input your message."
        self.fields['message'].widget.attrs['class'] = 'form-control'


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ["title", "content", "photo", "photo2", "photo3"]

