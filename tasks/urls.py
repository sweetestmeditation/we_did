from django.urls import path
from .views import TaskList, TaskDetail, TaskCreate, TaskUpdate, TaskDeleteView  # Make sure the import is correct

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='task-detail'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('delete-task/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),  # Make sure the view name is correct
]




