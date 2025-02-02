from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import News
from django.http import HttpResponse
from django.template import loader

from django.contrib.auth import login, authenticate
# Подключение различных модулей некоторые необязательны забыл удалить

# Пример модели
class BlogListView(ListView):
    model = News
    template_name = 'news.html'

class BlogDetailView(DetailView):
    model = News
    template_name = 'post_detail.html'

class BlogCreateView(CreateView):
    model = News
    template_name = 'post_new.html'
    fields = ['title', 'author', 'body', 'image']

class BlogUpdateView(UpdateView):
    model = News
    template_name = "post_edit.html"
    fields = ["title", "body", 'image']

class BlogDeleteView(DeleteView):
    model = News
    template_name = 'post_delete.html'
    success_url = reverse_lazy('news')

class HomeView(ListView):
    model = News
    template_name = 'index.html'

class ExitView(ListView):
    model = News
    template_name = 'exit.html'

class ActivitiesView(ListView):
    model = News
    template_name = 'activities.html'




