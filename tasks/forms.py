from django import forms
from .models import TaskAttachment

class TaskAttachmentForm(forms.ModelForm):
    class Meta:
        model = TaskAttachment
        fields = ['attachment']
