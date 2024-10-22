from django.conf import settings
from django.views.generic import ListView, DetailView, CreateView, TemplateView
from .models import BlogPost, Comment

from django.views.generic import FormView, DeleteView, UpdateView
from django.urls import reverse_lazy

from .forms import ContactForm, BlogPostForm, CommentCreateForm
from django.contrib import messages
from django.core.mail import EmailMessage

from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required

from django.shortcuts import redirect, get_object_or_404

import os


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = 'orderby_records'
    queryset = BlogPost.objects.order_by('-updated_at')
    # queryset = BlogPost.objects.prefetch_related("tags").order_by('-updated_at')
    paginate_by = 4


class BlogDetail(DetailView):
    template_name = "detail.html"
    model = BlogPost

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blogpost = self.object
        context["comment_list"] = (
            Comment.objects.select_related("comment_to").filter(comment_to=blogpost)
        )
        context["comment_form"] = CommentCreateForm

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

