from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import BlogPost, Comment, Like, Category, ClientIP
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
from django.http import HttpResponse, HttpResponseRedirect, Http404, HttpResponseForbidden

import os
import pytz
from django.utils import timezone
import json

import datetime
from ipware import get_client_ip

from django.contrib.gis.geoip2 import GeoIP2

def save_clientIP(request):
    client_addr, _ = get_client_ip(request)
    g = GeoIP2()
    try:
        city_dict = g.city(client_addr)
        city = city_dict['city']
        country_code = city_dict['country_code']
        country_name = city_dict['country_name']
    except Exception as e:
        city = None
        country_code = None
        country_name = None
    clientIP = ClientIP.objects.create(ip=client_addr, city=city, country_code=country_code, country_name=country_name, page=request.get_full_path())
    if request.user.id:
        clientIP.user = request.user
        clientIP.save()
    return clientIP


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

        posted_from = self.request.POST.get('posted_from', '')
        posted_to = self.request.POST.get('posted_to', '')

        try:
            datetime.datetime.strptime(posted_from, "%Y-%m-%d")
        except ValueError:
            posted_from = ""

        try:
            datetime.datetime.strptime(posted_to, "%Y-%m-%d")
        except ValueError:
            posted_to = ""


        if "reset" in request.POST:
            form_value = [
                None, None, None, False, None, None, None,
            ]
        else:
            form_value = [
                self.request.POST.get('author', None),
                self.request.POST.get('title', None),
                self.request.POST.get('content', None),
                self.request.POST.get('friends_post', False) == "on",
                self.request.POST.get('category', None),
                posted_from,
                posted_to,
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
        friends_post = False
        category = ''
        posted_from = ''
        posted_to = ''

        save_clientIP(self.request)

        search_words = False
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            if form_value:
                if (len(form_value) > 0) and form_value[0]:
                    author = form_value[0]
                    search_words = True
                else:
                    author = ''
                if (len(form_value) > 1) and form_value[1]:
                    title = form_value[1]
                    search_words = True
                else:
                    title = ''
                if (len(form_value) > 2) and form_value[2]:
                    content = form_value[2]
                    search_words = True
                else:
                    content = ''
                if (len(form_value) > 3) and form_value[3]:
                    friends_post = form_value[3]
                    search_words = True
                else:
                    friends_post = False
                if (len(form_value) > 4) and form_value[4]:
                    category = form_value[4].strip()
                    search_words = True
                else:
                    category = ''
                if (len(form_value) > 5) and form_value[5]:
                    posted_from = form_value[5]
                    search_words = True
                else:
                    posted_from = ''
                if (len(form_value) > 6) and form_value[6]:
                    posted_to = form_value[6]
                    search_words = True
                else:
                    posted_to = ''

        if len(author) != 0 and author[0]:
            context['site_subtitle'] = "auther: " + author

        default_data = {
            'author': author,
            'title': title,
            'content': content,
            'friends_post': friends_post,
            'category': category,
            'posted_from': posted_from,
            'posted_to': posted_to,
        }
        search_form = SearchForm(initial=default_data)
        context['search_words'] = search_words
        context['search_form'] = search_form
        context['category'] = category
        try:
            context['posted_from'] = datetime.datetime.strptime(posted_from, "%Y-%m-%d")
        except ValueError:
            context['posted_from'] = None
        try:
            context['posted_to'] = datetime.datetime.strptime(posted_from, "%Y-%m-%d")
        except ValueError:
            context['posted_to'] = None
        return context

    def get_queryset(self, **kwargs):

        author = ''
        title = ''
        content = ''
        category= ''
        friends_post = False
        posted_from = ''
        posted_to = ''

        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            if form_value:
                print("form_value")
                print(form_value)
                if (len(form_value) > 0) and form_value[0]:
                    author = form_value[0]
                else:
                    author = ''
                if (len(form_value) > 1) and form_value[1]:
                    title = form_value[1]
                else:
                    title = ''
                if (len(form_value) > 2) and form_value[2]:
                    content = form_value[2]
                else:
                    content = ''
                if (len(form_value) > 3) and form_value[3]:
                    friends_post = form_value[3]
                else:
                    friends_post = False
                if (len(form_value) > 4) and form_value[4]:
                    category = form_value[4].strip()
                else:
                    category = ''
                if (len(form_value) > 5) and form_value[5]:
                    posted_from = datetime.datetime.strptime(form_value[5], "%Y-%m-%d")
                else:
                    posted_from = None
                if (len(form_value) > 6) and form_value[6]:
                    posted_to = datetime.datetime.strptime(form_value[6], "%Y-%m-%d") + datetime.timedelta(days=1)
                else:
                    posted_to = None

        if len(author) != 0 and author[0]:
            if CustomUser.objects.filter(username__icontains=author).count()==0:
                condition_user = Q(user=None)
            else:
                users = CustomUser.objects.filter(username__icontains=author)
                condition_user = Q(user__in=users)
        else:
            condition_user = None

        if len(title) != 0 and title[0]:
            condition_title = Q(title__icontains=title)
        else:
            condition_title = None

        if len(category) != 0 and category[0]:
            if category == "__no_category":
                condition_category = Q(category__isnull=True)
            else:
                condition_category = Q(category__name=category)
        else:
            condition_category = None

        if len(content) != 0 and content[0]:
            condition_content = Q(content__icontains=content)
        else:
            condition_content = None

        if posted_from and posted_to:
            condition_posted_at = Q(created_at__range=[posted_from, posted_to])
        elif posted_from:
            condition_posted_at = Q(created_at__gte=posted_from)
        elif posted_to:
            condition_posted_at = Q(created_at__lte=posted_to)
        else:
            condition_posted_at = None

        if self.request.user.id:
            queryset = BlogPost.with_state(self.request.user.id).select_related('category').prefetch_related('comments').filter(Q_friends(self.request.user.friends()) | Q(user = self.request.user)).order_by('-created_at')
        else:
            queryset = BlogPost.with_state(self.request.user.id).select_related('category').prefetch_related('comments').filter(Q_open()).order_by('-created_at')

        if condition_user:
            queryset = queryset.filter(condition_user)

        if condition_title:
            queryset = queryset.filter(condition_title)

        if condition_category:
            queryset = queryset.filter(condition_category)

        if condition_content:
            queryset = queryset.filter(condition_content)

        if friends_post:
            if self.request.user.id:
                queryset = queryset.filter(Q(user__in=self.request.user.friends()))
            else:
                if 'form_value' in self.request.session:
                    form_value = self.request.session['form_value']
                    if form_value:
                        if (len(form_value) > 3) and form_value[3]:
                            self.request.session['form_value'][3] = False

        if condition_posted_at:
            queryset = queryset.filter(condition_posted_at)

        return queryset


class BlogDetail(DetailView):
    template_name = "detail.html"
    model = BlogPost

    def get(self, request, *args, **kwargs):
        try:
            save_clientIP(request)
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


class ContactSentView(TemplateView):
    template_name = "contact_sent.html"


class ContactView(FormView):
    template_name = "contact.html"
    form_class = ContactForm
    success_url = reverse_lazy('blog:contact_sent')

    def get_form_kwargs(self):
        save_clientIP(self.request)
        kwargs = super(ContactView, self).get_form_kwargs()
        if self.request.user.is_authenticated:
            kwargs['initial']['name'] = self.request.user.username
            kwargs['initial']['email'] = self.request.user.email
        return kwargs

    def form_valid(self, form):
        name = form.cleaned_data['name']
        email = form.cleaned_data['email']
        title = form.cleaned_data['title']
        message = form.cleaned_data['message']
        client_addr, _ = get_client_ip(self.request)
        g = GeoIP2()
        try:
            city_dict = g.city(client_addr)
            city = city_dict['city']
            country_code = city_dict['country_code']
            country_name = city_dict['country_name']
        except Exception as e:
            city = None
            country_code = None
            country_name = None

        subject = '[' + self.request.META['HTTP_HOST'] + '] Message: {}'.format(title)
        message = \
            'client info.: {4}, {5}, {6}, {7}\nsender: {0}\nmail: {1}\ntitle: {2}\nmessage:\n{3}'\
            .format(name, email, title, message, client_addr, city, country_code, country_name)

        from_email = settings.EMAIL_ADMIN
        to_list = [settings.EMAIL_ADMIN]

        message = EmailMessage(subject=subject,
                                body=message,
                                from_email=from_email,
                                to=to_list)
        message.send()
        messages.success(
            self.request, 'Message was sent properly. subject:{}'.format(title))

        return super().form_valid(form)


@method_decorator(login_required,name='dispatch')
class CreateBlogPostView(CreateView):
    form_class = BlogPostForm
    template_name = "post.html"

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        save_clientIP(self.request)
        kwgs["initial"]["category"] = Category.objects.filter(owner=self.request.user)
        return kwgs

    def form_valid(self, form):
        postdata = form.save(commit=False)
        postdata.user = self.request.user
        postdata.save()
        if 'form_value' in self.request.session:
            form_value = self.request.session['form_value']
            if form_value:
                if (len(form_value) > 4) and form_value[4]:
                    self.request.session['form_value'][4] = postdata.category

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
        save_clientIP(request)
        return super().delete(request, *args, **kwargs)

@method_decorator(login_required,name='dispatch')
class UpdateBlogPostView(UpdateView):
    model = BlogPost
    form_class = BlogPostForm
    template_name = "update.html"

    def get_form_kwargs(self, *args, **kwargs):
        kwgs = super().get_form_kwargs(*args, **kwargs)
        kwgs["initial"]["category"] = Category.objects.filter(owner=self.request.user)
        save_clientIP(self.request)
        return kwgs

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

class MiscView(TemplateView):
    template_name = "misc.html"

    def get(self, request, **kwargs):
        clientIP = save_clientIP(self.request)
        context = {
            'clientIP': clientIP,
        }
        return self.render_to_response(context)


class FireworksView(TemplateView):
    template_name = "fireworks.html"


def csrf_failure(request, reason=""):
    # msg = "CSRF Error found and redirected to Top Page."
    # messages.warning(request, msg)
    return HttpResponseRedirect(reverse_lazy('blog:index'))
