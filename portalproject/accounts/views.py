from django.shortcuts import render, redirect
from django.views.generic import View, DetailView
from .models import CustomUser, Connection
from blog.models import BlogPost
from django.contrib import messages

from .forms import UsernameChangeForm, IconChangeForm, IntroductionChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required

from urllib.parse import urlencode
import datetime
import json
from django.http import HttpResponse


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
        if 'return_url' in request.session:
            context["return_url"] = request.session["return_url"]
        else:
            if 'HTTP_REFERER' in request.META:
                request.session["return_url"] = request.META['HTTP_REFERER']
            else:
                request.session["return_url"] = "blog:index"
            context["return_url"] = request.session["return_url"]

        context['following'] = Connection.objects.filter(follower=request.user).count()
        context['follower'] = Connection.objects.filter(following=request.user).count()
        context['friends'] = request.user.friends().count()
        context['posts'] = BlogPost.objects.filter(user=request.user).count()

        return render(request, 'accounts/profile.html', context)


class IntroductionChangeView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        context = {}
        context["current_introduction"] = request.user.introduction
        form = IntroductionChangeForm({"introduction": request.user.introduction})
        context["form"] = form
        return render(request, 'accounts/update_introduction.html', context)


    def post(self, request, *args, **kwargs):
        context = {}
        form = IntroductionChangeForm(request.POST)

        if form.is_valid():
            introduction = form.cleaned_data["introduction"]
            user_obj = CustomUser.objects.get(username=request.user.username)
            user_obj.introduction = introduction
            user_obj.save()
            messages.info(request,"Introduction has changed for {}".format(user_obj.username))

            return redirect('accounts:profile')
        else:
            context["form"] = form

            return render(request, 'accounts/update_introduction.html', context)


class TargetUserView(View):
    template_name = "user.html"
    model = CustomUser

    def get(self, request, *args, **kwargs):
        context = {}
        context["user"] = request.user

        if "username" in kwargs:
            target_username = kwargs["username"]
        else:
            target_username = request.user
        try:
            user_obj = CustomUser.objects.get(username=target_username)
        except Exception as e:
            return HttpResponseRedirect(reverse_lazy('blog:index'))


        if user_obj == None:
            return redirect('blog:index')
        context["target_user"] = user_obj
        context['following'] = Connection.objects.filter(follower=user_obj).count()
        context['follower'] = Connection.objects.filter(following=user_obj).count()
        context['posts'] = BlogPost.objects.filter(user=user_obj).count()

        if request.user.username is not target_username:
            result = Connection.objects.filter(follower__username=request.user.username).filter(following__username=target_username)
            context['connected'] = True if result else False

        if 'HTTP_REFERER' in request.META:
            request.session["return_url"] = request.META['HTTP_REFERER']
        else:
            request.session["return_url"] = "blog:index"
        context["return_url"] = request.session["return_url"]
        request.session["return_url"] = request.path

        return render(request, 'accounts/user.html', context)

    def post(self, request, *args, **kwargs):
        context = {}
        context["user"] = request.user
        target_username = request.POST['target_user']
        user_obj = CustomUser.objects.get(username=target_username)
        context["target_user"] = user_obj
        if 'return_url' in request.POST:
            context["return_url"] = request.POST['return_url']
            request.session["return_url"] = context["return_url"]
        else:
            context["return_url"] = request.session["return_url"]
        request.session["return_url"] = request.path

        context['following'] = Connection.objects.filter(follower=user_obj).count()
        context['follower'] = Connection.objects.filter(following=user_obj).count()
        context['posts'] = BlogPost.objects.filter(user=user_obj).count()

        if request.user.username is not target_username:
            result = Connection.objects.filter(follower__username=request.user.username).filter(following__username=target_username)
            context['connected'] = True if result else False

        return render(request, 'accounts/user.html', context)


@login_required
def follow_view(request, *args, **kwargs):

    try:
        follower = CustomUser.objects.get(username=request.user.username)
        following = CustomUser.objects.get(username=kwargs['username'])
    except CustomUser.DoesNotExist:
        messages.warning(request, '{} does not exst.'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('blog:index'))

    if follower == following:
        messages.warning(request, "you can't follow yourself.")
    else:
        _, created = Connection.objects.get_or_create(follower=follower, following=following)

        if (created):
            messages.success(request, '{} was followed.'.format(following.username))
        else:
            messages.warning(request, 'You are already following {}'.format(following.username))

    params = {
        'username': following.username,
    }
    return HttpResponseRedirect(reverse_lazy('accounts:target_user_w_username', kwargs=params))


@login_required
def unfollow_view(request, *args, **kwargs):

    try:
        follower = CustomUser.objects.get(username=request.user.username)
        following = CustomUser.objects.get(username=kwargs['username'])
        if follower == following:
            messages.warning(request, "you can't unfollow yourself.")
        else:
            unfollow = Connection.objects.get(follower=follower, following=following)
            unfollow.delete()
            messages.success(request, '{} was unfollowed.'.format(following.username))

    except CustomUser.DoesNotExist:
        messages.warning(request, '{} does not exst.'.format(kwargs['username']))
        return HttpResponseRedirect(reverse_lazy('blog:index'))
    except Connection.DoesNotExist:
        messages.warning(request, '{} was not followed.'.format(following.username))

    params = {
        'username': following.username,
    }
    return HttpResponseRedirect(reverse_lazy('accounts:target_user_w_username', kwargs=params))


class ProfileDetail(LoginRequiredMixin, DetailView):
    model = CustomUser
    template_name = 'user.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(ProfileDetail, self).get_context_data(**kwargs)
        username = self.kwargs['username']
        context['username'] = username
        context['user'] = get_current_user(self.request)
        context['following'] = Connection.objects.filter(follower__username=username).count()
        context['follower'] = Connection.objects.filter(following__username=username).count()

        if username is not context['user'].username:
            result = Connection.objects.filter(follower__username=context['user'].username).filter(following__username=username)
            context['connected'] = True if result else False

        return context


class FollowPopupView(DetailView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def post(self, request, *args, **kwargs):
        return_value = None
        try:
            results = []
            if kwargs['follow'] == 'followings':
                follows = Connection.objects.filter(follower__username=kwargs['username']).order_by('-created_at')
                for follow in follows:
                    result = {}
                    result['username'] = follow.following.username
                    result['created_at'] = datetime.datetime.strftime(follow.created_at, "%Y-%m-%dT%H:%M:%SZ")

                    if follow.following.icon_small:
                        result['icon'] = follow.following.icon_small.url
                    else:
                        result['icon'] = ""
                    results.append(result)

            elif kwargs['follow'] == 'follower':
                follows = Connection.objects.filter(following__username=kwargs['username']).order_by('-created_at')
                for follow in follows:
                    result = {}
                    result['username'] = follow.follower.username
                    result['created_at'] = datetime.datetime.strftime(follow.created_at, "%Y-%m-%dT%H:%M:%SZ")

                    if follow.follower.icon_small:
                        result['icon'] = follow.follower.icon_small.url
                    else:
                        result['icon'] = ""
                    results.append(result)

            else:
                me = CustomUser.objects.filter(username=kwargs['username'])[0]
                friends = me.friends()
                for friend in friends:
                    result = {}
                    result['username'] = friend.username
                    result['created_at'] = datetime.datetime.strftime(friend.date_joined, "%Y-%m-%dT%H:%M:%SZ")

                    if friend.icon_small:
                        result['icon'] = friend.icon_small.url
                    else:
                        result['icon'] = ""
                    results.append(result)

            return_value = json.dumps(results, default=str)

        except Connection.DoesNotExist:
            pass

        return HttpResponse(return_value, status=200)
