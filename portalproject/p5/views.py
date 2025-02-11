from django.shortcuts import render
from django.views.generic import TemplateView, DetailView, ListView
from .models import Page


class P5View(ListView):
    template_name = "p5.html"

    def get_queryset(self):
        queryset = Page.objects.all()

class TmpView(TemplateView):
    template_name = "tmp.html"

# Create your views here.
class AppView(TemplateView):
    template_name = "app.html"
