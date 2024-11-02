from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from .models import CustomUser
from django.contrib import messages

from .forms import UsernameChangeForm, IconChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin


class UsernameChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["current_username"] = request.user.username
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


class IconChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["current_icon"] = request.user.icon
        form = IconChangeForm()
        context["form"] = form
        return render(request, 'accounts/update_icon.html', context)


    def post(self, request, *args, **kwargs):
        context = {}
        form = IconChangeForm(request.POST)

        if form.is_valid():
            icon = request.FILES["icon"]
            user_obj = CustomUser.objects.get(username=request.user.username)
            user_obj.icon = icon
            user_obj.save()
            user_obj.icon_small.generate()
            user_obj.save()
            messages.info(request,"icon has changed for {}".format(user_obj.username))

            return redirect('blog:index')
        else:
            context["form"] = form

            return render(request, 'accounts/update_icon.html', context)


class CustomUserView(LoginRequiredMixin, View):
    template_name = "profile.html"
    model = CustomUser

    def get(self, request, *args, **kwargs):
        context = {}
        context["user"] = request.user
        return render(request, 'accounts/profile.html', context)
