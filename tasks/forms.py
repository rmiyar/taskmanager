from django import forms
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ['title', 'description', 'date', 'time', 'priority']
        widgets = {
            'title': forms.TextInput(attrs={
                'placeholder': 'Título de la tarea'
            }),
            'description': forms.Textarea(attrs={
                'placeholder': 'Descripción de la tarea...',
                'rows': 4
            }),
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'priority': forms.Select(),
        }
