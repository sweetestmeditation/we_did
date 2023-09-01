from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from .models import Task

# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_use = True

    def get_success_url(self):
        return reverse_lazy('task-list')

class TaskList(ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

class TaskDetail(DetailView):
    model = Task
    context_object_name = 'task'

class TaskCreate(CreateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-list')

class TaskUpdate(UpdateView):
    model = Task
    fields = '__all__'
    success_url = reverse_lazy('task-list')  

class TaskDeleteView(DeleteView):  # Renamed to avoid conflict with built-in DeleteView
    model = Task
    context_object_name = 'task'
    success_url = reverse_lazy('task-list')

