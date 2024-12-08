from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import BlogPost, Comment, Like
from accounts.models import CustomUser, Connection

from django.views.generic import FormView, DeleteView, UpdateView
from django.urls import reverse_lazy, reverse

from .forms import ContactForm, BlogPostForm, CommentCreateForm, SearchForm
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import redirect, get_object_or_404
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect, Http404

import os
import pytz
from django.utils import timezone
import json

import datetime


def Q_open():
    return Q(is_public=True) & Q(only_friends=False)


def Q_friends(friends):
    return Q(is_public=True) & (Q(user__in=friends) | Q(only_friends=False))


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = 'orderby_records'
    # queryset = BlogPost.objects.prefetch_related("tags").order_by('-updated_at')
    paginate_by = settings.PAGINATE_BY

    def get_queryset(self):
        if self.request.user.id:
            queryset = BlogPost.with_state(self.request.user.id).prefetch_related('comments').filter(Q_friends(self.request.user.friends()) | Q(user = self.request.user)).order_by('-created_at')
        else:
            queryset = BlogPost.with_state(self.request.user.id).prefetch_related('comments').filter(Q_open()).order_by('-created_at')

        return queryset


class CustomView(ListView):
    template_name = "index.html"
    context_object_name = 'orderby_records'
    # queryset = BlogPost.objects.prefetch_related("tags").order_by('-updated_at')
    paginate_by = settings.PAGINATE_BY

    def post(self, request, *args, **kwargs):

        if "reset" in request.POST:
            form_value = [
                None, None, None,
            ]
        else:
            form_value = [
                self.request.POST.get('author', None),
                self.request.POST.get('title', None),
                self.request.POST.get('content', None),
            ]

        request.session['form_value'] = form_value

        self.request.GET = self.request.GET.copy()
        self.request.GET.clear()

        return self.get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        author = ''
        title = ''
        content = ''

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            if form_value[0]:
                author = form_value[0]
            else:
                author = ''
            if form_value[1]:
                title = form_value[1]
            else:
                title = ''
            if form_value[2]:
                content = form_value[2]
            else:
                content = ''

        if len(author) != 0 and author[0]:
            context['site_subtitle'] = "auther: " + author

        default_data = {
            'author': author,
            'title': title,
            'content': content,
        }
        search_form = SearchForm(initial=default_data)
        context['search_form'] = search_form
        return context

    def get_queryset(self, **kwargs):

        author = ''
        title = ''
        content = ''

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            if form_value[0]:
                author = form_value[0]
            else:
                author = ''
            if form_value[1]:
                title = form_value[1]
            else:
                title = ''
            if form_value[2]:
                content = form_value[2]
            else:
                content = ''

        if len(author) != 0 and author[0]:
            if CustomUser.objects.filter(username=author).count()==0:
                condition_user = Q(user=None)
            else:
                user = CustomUser.objects.filter(username=author)[0]
                condition_user = Q(user=user)
        else:
            condition_user = None

        if len(title) != 0 and title[0]:
            condition_title = Q(title__icontains=title)
        else:
            condition_title = None

        if len(content) != 0 and content[0]:
            condition_content = Q(content__icontains=content)
        else:
            condition_content = None

        if self.request.user.id:
            queryset = BlogPost.with_state(self.request.user.id).prefetch_related('comments').filter(Q_friends(self.request.user.friends()) | Q(user = self.request.user)).order_by('-created_at')
        else:
            queryset = BlogPost.with_state(self.request.user.id).prefetch_related('comments').filter(Q_open()).order_by('-created_at')

        if condition_user:
            queryset = queryset.filter(condition_user)

        if condition_title:
            queryset = queryset.filter(condition_title)

        if condition_content:
            queryset = queryset.filter(condition_content)

        return queryset


class BlogDetail(DetailView):
    template_name = "detail.html"
    model = BlogPost

    def get(self, request, *args, **kwargs):
        try:
            result = super().get(request, *args, **kwargs)
            blogpost = self.object
        except Exception as e:
            msg = str(e) + ": {}".format(request.path)
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse_lazy('blog:index'))
        blogpost = self.object

        if blogpost.is_public == False:
            if request.user.id == None:
                msg = "Sorry, you have no right to see: " + ": {}".format(request.path)
                messages.warning(request, msg)
                return HttpResponseRedirect(reverse_lazy('blog:index'))
            else:
                if request.user != blogpost.user:
                    msg = "Sorry, you have no right to see: " + ": {}".format(request.path)
                    messages.warning(request, msg)
                    return HttpResponseRedirect(reverse_lazy('blog:index'))

        if blogpost.only_friends == True and request.user != blogpost.user:
            if request.user.id == None:
                msg = "Sorry, you have no right to see: " + ": {}".format(request.path)
                messages.warning(request, msg)
                return HttpResponseRedirect(reverse_lazy('blog:index'))
            try:
                typeA = Connection.objects.filter(follower=request.user, following=blogpost.user)
                typeB = Connection.objects.filter(follower=blogpost.user, following=request.user)
                print("typeA: ", str(typeA))
                print("typeB: ", str(typeB))
                if typeA.count() == 0:
                    print("typeA is None")
            except Connection.DoesNotExist:
                msg = "Sorry, you have no right to see: " + ": {}".format(request.path)
                messages.warning(request, msg)
                return HttpResponseRedirect(reverse_lazy('blog:index'))

        request.session["return_url"] = request.path
        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogpost = self.object
        if blogpost.is_public == False:
            context["private"] = True
        else:
            context["private"] = False

        context["comment_list"] = (
            Comment.objects.select_related("comment_to").filter(comment_to=blogpost).prefetch_related("reply_to").order_by('-created_at')
        )
        if self.request.user:
            context["blogpost"] = BlogPost.with_state(self.request.user.id).filter(id=blogpost.id)[0]
        else:
            context["blogpost"] = None

        context["form"] = CommentCreateForm


        return context


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact')

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']

        subject = 'Message: {}'.format(title)
        message = \
            'sender: {0}\nmail: {1}\ntitle: {2}\nmessage:\n{3}'\
            .format(name, email, title, message)

        from_email = settings.EMAIL_ADMIN
        to_list = [settings.EMAIL_ADMIN]

        message = EmailMessage(subject=subject,
                                body=message,
                                from_email=from_email,
                                to=to_list)
        message.send()
        messages.success(
            self.request, 'Message was sent properly')

        return super().form_valid(form)


@method_decorator(login_required,name='dispatch')
class CreateBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = "post.html"

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()

        return super().form_valid(form)

@method_decorator(login_required,name='dispatch')
class PostSuccessView(TemplateView):
    template_name = "post_success.html"


@method_decorator(login_required,name='dispatch')
class BlogDeleteView(DeleteView):
    model = BlogPost
    template_name = "delete.html"
    success_url = reverse_lazy('blog:index')

    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required,name='dispatch')
class UpdateBlogPostView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "update.html"

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()

        return super().form_valid(form)


@method_decorator(login_required,name='dispatch')
class CommentCreate(CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        post = get_object_or_404(BlogPost, pk=post_pk)

        comment = form.save(commit=False)
        comment.commenter = self.request.user
        comment.comment_to = post
        comment.save()

        return redirect('blog:blog_detail', pk=post_pk)


@method_decorator(login_required,name='dispatch')
class CommentCreate2(CreateView):
    model = Comment
    form_class = CommentCreateForm

    def form_valid(self, form):
        post_pk = self.kwargs.get('pk')
        parent = get_object_or_404(Comment, pk=post_pk)

        comment = form.save(commit=False)
        comment.commenter = self.request.user
        comment.reply_to = parent
        comment.save()

        return redirect('blog:comment_detail', pk=post_pk)


class CommentDetail(DetailView):
    template_name = "comment.html"
    model = Comment

    def get(self, request, *args, **kwargs):
        try:
            result = super().get(request, *args, **kwargs)
            comment = self.object
        except Exception as e:
            msg = str(e) + ": {}".format(request.path)
            messages.warning(request, msg)
            return HttpResponseRedirect(reverse_lazy('blog:index'))
        comment = self.object

        return result

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        comment = self.object

        context["comment_list"] = (
            Comment.objects.select_related("reply_to").filter(reply_to=comment).prefetch_related("replies").order_by('-created_at')
        )
        context["parent_list"] = []
        current = comment
        while True:
            if current.comment_to:
                context["parent_list"].append(current.comment_to)
                break
            else:
                if current.reply_to:
                    current = current.reply_to
                    context["parent_list"].append(current)
                else:
                    break


        context["form"] = CommentCreateForm

        return context


class CreateLikeView(LoginRequiredMixin, CreateView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def post(self, request, *args, **kwargs):
        return_value = None
        try:
            Like.objects.create(user_id=kwargs['user_id'], blogpost_id=kwargs['blogpost_id'])
        except Exception as e:
            logging.critical('An unauthorized article was accessed')

        try:
            blogpost = BlogPost.with_state(kwargs['user_id']).get(pk=kwargs['blogpost_id'])
            return_value = json.dumps({'like_cnt': blogpost.like_cnt, 'liked_by_me': blogpost.liked_by_me})
            print(f'LikeCreateView return_value[{type(return_value)}]: ', return_value)
        except BlogPost.DoesNotExist:
            logging.critical('An unauthorized article was accessed')

        return HttpResponse(return_value, status=200)


class DeleteLikeView(LoginRequiredMixin, DeleteView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def post(self, request, *args, **kwargs):
        return_value = None
        try:
            Like.objects.filter(user_id=kwargs['user_id'], blogpost_id=kwargs['blogpost_id']).delete()
            blogpost = BlogPost.with_state(kwargs['user_id']).get(pk=kwargs['blogpost_id'])
            return_value = json.dumps({'like_cnt': blogpost.like_cnt, 'liked_by_me': blogpost.liked_by_me})
            print(f'LikeDeleteView return_value[{type(return_value)}]: ', return_value)
        except BlogPost.DoesNotExist:
            logging.critical('An unauthorized article was accessed')

        return HttpResponse(return_value, status=200)


class LikesView(DetailView):
    model = BlogPost
    template_name = "likes.html"
    context_object_name = 'orderby_records'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogpost = self.object

        print(kwargs)
        context["like_list"] = (
            Like.objects.select_related("user").filter(blogpost=blogpost).order_by('-created_at')
        )
        print(context["like_list"])

        return context


class LikesPopupView(DetailView):
    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset

    def post(self, request, *args, **kwargs):
        return_value = None
        try:
            likes = Like.objects.select_related("user").filter(blogpost_id=kwargs['pk']).order_by('-created_at')
            results = []
            for like in likes:
                result = {}
                result['username'] = like.user.username
                result['created_at'] = datetime.datetime.strftime(like.created_at, "%Y-%m-%dT%H:%M:%SZ")
                if like.user.icon_small:
                    result['icon'] = like.user.icon_small.url
                else:
                    result['icon'] = ""
                results.append(result)
            print(results)
            return_value = json.dumps(results, default=str)
        except Like.DoesNotExist:
            pass

        return HttpResponse(return_value, status=200)
