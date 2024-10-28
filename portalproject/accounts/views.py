from django.shortcuts import render, redirect
from django.views.generic import View
from .models import CustomUser
from django.contrib import messages

from .forms import UsernameChangeForm


class UsernameChangeView(View):
    def get(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm()
        context["form"] = form
        return render(request, 'accounts/update_username.html', context)


    def post(self, request, *args, **kwargs):
        context = {}
        form = UsernameChangeForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data["username"]
            user_obj = CustomUser.objects.get(username=request.user.username)
            user_obj.username = username
            user_obj.save()
            messages.info(request,"username has changed")

            return redirect('blog:index')
        else:
            context["form"] = form

            return render(request, 'accounts/update_username.html', context)
