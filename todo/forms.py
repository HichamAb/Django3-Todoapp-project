from django import forms
from .models import TodoModel

class TodoForm(forms.ModelForm) :
    class Meta : 
        model = TodoModel
        fields = [
            'title','note','is_important'
        ]