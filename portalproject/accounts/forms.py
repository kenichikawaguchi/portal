from django import forms
from .models import CustomUser


class UsernameChangeForm(forms.ModelForm):

    class Meta:
        model  = CustomUser
        fields = ("username",)

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
