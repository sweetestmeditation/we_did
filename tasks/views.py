from django import forms

class DeleteTaskForm(forms.Form):
    action = forms.ChoiceField(choices=[('Delete', 'Delete'), ('Archive', 'Archive')], widget=forms.RadioSelect)

from typing import Any, Dict
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.views.generic.base import View
from django.shortcuts import redirect, get_object_or_404
from .models import Task
from .forms import TaskAttachmentForm
from django.db import models
from django.urls import reverse
from django.http import HttpResponseRedirect


# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'tasks/login.html'
    fields = '__all__'
    redirect_authenticated_use = True

    def get_success_url(self):
        return reverse_lazy('task-list')
    
class RegisterPage(FormView):
    template_name = 'tasks/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('task-list')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        return super(RegisterPage, self).get(*args, **kwargs)

class TaskList(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'task_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = super().get_queryset().filter(user=self.request.user)
        search_input = self.request.GET.get('search-area')
        if search_input:
            queryset = queryset.filter(title__icontains=search_input)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['count'] = context['tasks'].filter(complete=False).count()
        return context

class TaskDetailView(DetailView):
    model = Task
    template_name = 'tasks/task_detail.html'
    context_object_name = 'task'

def task_detail(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    # Handle attachment form submission
    if request.method == 'POST':
        attachment_form = TaskAttachmentForm(request.POST, request.FILES)
        if attachment_form.is_valid():
            attachment = attachment_form.save(commit=False)
            attachment.task = task
            attachment.save()
            return redirect('task-detail', pk=task.pk)  # Redirect back to task detail page

    else:
        attachment_form = TaskAttachmentForm()

    return render(request, 'tasks/task_detail.html', {'task': task, 'attachment_form': attachment_form})

class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')

    def form_valid(self, form):
        form.instance.user = self.request.user 
        return super(TaskCreate, self).form_valid(form)

class TaskUpdate(UpdateView):
    model = Task
    fields = ['title', 'description', 'complete']
    success_url = reverse_lazy('task-list')  

class TaskDeleteView(FormView):
    template_name = 'tasks/task_confirm_delete.html'
    form_class = DeleteTaskForm  # Use the custom form for the delete/archive choice

    def form_valid(self, form):
        task = Task.objects.get(pk=self.kwargs['pk'])
        action = form.cleaned_data['action']  # Get the selected action from the form
        if action == 'Delete':
            task.delete()
        elif action == 'Archive':
            task.archived = True
            task.save()
        return HttpResponseRedirect(reverse('task-list'))

class UnarchiveTask(View):
    template_name = 'tasks/archive_task_list.html'
    fields = '__all__'

class TaskView(models.Model):
    # Your other fields
    archived = models.BooleanField(default=False)


"""def archive_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.archived = True
    task.save()
    return redirect('task-list')  # Redirect to your task list view

def unarchive_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    task.archived = False
    task.save()
    return redirect('task-list')  # Redirect to your task list view

def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id)
    
    # Set the archived field to True instead of deleting
    task.archived = True
    task.save()
    
    return redirect('task-list')
"""
def task_list(request):
    # Only fetch tasks that are not archived
    tasks = Task.objects.filter(archived=False)
    context = {'tasks': tasks}
    return render(request, 'task_list.html', context)

class ArchiveTask(View):
    def post(self, request, task_id):
        task = get_object_or_404(Task, pk=task_id)
        task.archived = True
        task.save()
        return redirect('task-list')  # Redirect to your task list view
    
class ArchiveTaskList(ListView):
    model = Task
    template_name = 'archive_task_list.html'
    context_object_name = 'archived_tasks'

    def get_queryset(self):
        return Task.objects.filter(archived=True)

