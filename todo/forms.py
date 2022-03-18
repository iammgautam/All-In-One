from django import forms
from todo.models import Todo



class TodoForm(forms.ModelForm):
    
    class Meta:
        model = Todo
        fields = ("title","description",'complete')
        widgets = {
            'title':forms.TextInput(attrs={'class':'todo-input','placeholder':'Add a Task Title'}),
            'description':forms.Textarea(attrs={'class':'todo-input','placeholder':'Add a Description'}),
            'complete': forms.CheckboxInput(attrs={'class': 'todo-input', 'label':'Complete:'}),
        }