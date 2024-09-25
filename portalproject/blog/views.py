from django.conf import settings
from django.views.generic import ListView, DetailView
from .models import BlogPost

from django.views.generic import FormView
from django.urls import reverse_lazy

from .forms import ContactForm
from django.contrib import messages
from django.core.mail import EmailMessage


class IndexView(ListView):
    template_name = "index.html"
    context_object_name = 'orderby_records'
    queryset = BlogPost.objects.order_by('-updated_at')
    paginate_by = 4

class BlogDetail(DetailView):
    template_name = "detail.html"
    model = BlogPost


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


