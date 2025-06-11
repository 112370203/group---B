from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Topic
from .models import NoteItem


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['name']

class NoteItemForm(forms.ModelForm):
    class Meta:
        model = NoteItem
        #fields = ['content', 'image']
        fields = ['title','content', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 3, 'placeholder': '輸入筆記內容'}),
            'title': forms.Textarea(attrs={'rows': 1, 'placeholder': '輸入筆記標題'}),

        }

class ShareTopicForm(forms.Form):
    email = forms.EmailField()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'w-full p-2 border border-gray-300 rounded'})