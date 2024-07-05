from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Comment, Post, User


class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = User


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'text': forms.Textarea({'rows': '5'}),
            'pub_date': forms.DateInput(
                format=('%Y-%m-%d'),
                attrs={'type': 'date'}
            )
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)


class ProfileEditForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username')
