from django import forms
from .models import BlogPost, Comment, Category
from django.core.exceptions import ValidationError


def check_date(value):
    try:
        datetime.datetime.strptime(value, "%Y-%m-%d")
    except ValueError:
        raise ValidationError('Input Date in "yyyy-mm-dd" format.')

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
        fields = ["title", "category", "content", "is_public", "only_friends", "photo", "photo2", "photo3"]

    def __init__(self, *args, **kwargs):
        tmp = kwargs.get('initial')['category']
        print(kwargs.get('instance'))
        if kwargs.get('instance') is not None:
            selected_category = kwargs.get('instance').category
        else:
            selected_category = None
        print("selected_category is " + str(selected_category))
        super().__init__(*args, **kwargs)
        choices = []
        choices.append((None, ""))
        for i in tmp:
            choices.append((i.id, i.name))
        self.fields['category'].choices = choices
        self.initial['category'] = selected_category
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
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


class SearchForm(forms.Form):

    author = forms.CharField(
        initial='',
        label='Author',
        required=False,
    )

    title = forms.CharField(
        initial='',
        label='Title',
        required=False,
    )

    category = forms.ChoiceField(
        initial='',
        label='Category',
        required=False,
        widget=forms.widgets.Select
    )

    content = forms.CharField(
        initial='',
        label='Content',
        required=False,
    )

    friends_post = forms.BooleanField(
        initial=False,
        label="Friends' Posts",
        required=False,
    )

    posted_from = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial='',
        label='Posted from',
        required=False,
        validators=[check_date],
        input_formats=['%Y-%m-%d'],
    )

    posted_to = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        initial='',
        label='Posted to',
        required=False,
        validators=[check_date],
        input_formats=['%Y-%m-%d'],
    )

    def __init__(self, *args, **kwargs):
        print(kwargs.get('instance'))
        if kwargs.get('instance') is not None:
            selected_category = kwargs.get('instance').category
        else:
            selected_category = None
        super().__init__(*args, **kwargs)
        self.fields['author'].widget.attrs['class'] = 'form-control'
        self.fields['title'].widget.attrs['class'] = 'form-control'
        self.fields['category'].widget.attrs['class'] = 'form-control'
        choices = ["", "__no_category"]
        for i in Category.objects.all().order_by('name').distinct().values_list('name'):
            choices.append(i[0])
        self.fields['category'].choices = choices
        self.initial['category'] = selected_category
        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['friends_post'].widget.attrs['class'] = 'form-check-input'
        self.fields['posted_from'].widget.attrs['class'] = 'form-control'
        self.fields['posted_from'].widget.attrs['placeholder'] = 'yyyy-mm-dd'
        self.fields['posted_to'].widget.attrs['class'] = 'form-control'
        self.fields['posted_to'].widget.attrs['placeholder'] = 'yyyy-mm-dd'

    def clean(self):
        cleaned_data = super().clean()
        posted_from = cleaned_data.get("posted_from")

        if posted_from:
            check_date(posted_from)

