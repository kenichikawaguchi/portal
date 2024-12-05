from django import forms
from .models import BlogPost, Comment


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
        fields = ["title", "content", "is_public", "only_friends", "photo", "photo2", "photo3"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['is_public'].widget.attrs['class'] = 'form-check-input'
        self.fields['only_friends'].widget.attrs['class'] = 'form-check-input'
        self.fields['photo'].widget.attrs['class'] = 'form-control'
        self.fields['photo2'].widget.attrs['class'] = 'form-control'
        self.fields['photo3'].widget.attrs['class'] = 'form-control'

class CommentCreateForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["text"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
