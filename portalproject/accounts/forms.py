from django import forms
from .models import CustomUser
from blog.models import Category

from markdownx.widgets import MarkdownxWidget


class UsernameChangeForm(forms.ModelForm):

    class Meta:
        model  = CustomUser
        fields = ("username", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."

    def clean_username(self):
        username = self.cleaned_data.get('username')
        username_qs = CustomUser.objects.filter(username=username)
        if username_qs.exists():
            raise forms.ValidationError("Username already exists")
        return username


class IconChangeForm(forms.ModelForm):

    class Meta:
        model  = CustomUser
        fields = ("icon", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."

    def clean_icon(self):
        icon = self.cleaned_data.get('icon')
        return icon


class IntroductionChangeForm(forms.ModelForm):

    class Meta:
        model  = CustomUser
        fields = ("introduction", )
        widgets = {
            "introduction": MarkdownxWidget(),
        }

    def clean_icon(self):
        introduction = self.cleaned_data.get('introduction')
        return introduction


class CategoryChangeForm(forms.ModelForm):

    class Meta:
        model  = Category
        fields = ("owner", "name", )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        user = kwargs.get('user')
        for field in self.fields.values():
            field.widget.attrs['class'] = "form-control"
            field.widget.attrs['placeholder'] = "150 characters or fewer. Letters, digits and @/./+/-/_ only."
