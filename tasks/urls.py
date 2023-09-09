from django.urls import path
from django.contrib.auth.views import LogoutView  # Import LogoutView
from .views import (
    TaskList,
    TaskDetailView,
    TaskCreate,
    TaskUpdate,
    TaskDeleteView,
    CustomLoginView,
    RegisterPage,
    ArchiveTaskList,
    ArchiveTask,  # Import the archive_task view
    # UnarchiveTask,  # Import the unarchive_task view
)

urlpatterns = [
    path('', TaskList.as_view(), name='task-list'),  # This makes the home page accessible at the root URL
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),  # Use LogoutView here
    path('register/', RegisterPage.as_view(), name='register'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),
    path('create-task/', TaskCreate.as_view(), name='task-create'),
    path('update-task/<int:pk>/', TaskUpdate.as_view(), name='task-update'),
    path('delete-task/<int:pk>/', TaskDeleteView.as_view(), name='task-delete'),
    path('archive-task-list/', ArchiveTaskList.as_view(), name='archive-task-list'),
    path('archive-task/<int:task_id>/', ArchiveTask.as_view(), name='archive-task'),

]








