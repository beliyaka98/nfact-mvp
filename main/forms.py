from django.forms import ModelForm
from django.contrib.auth.models import User
from .models import Challenge
from django.contrib.auth.forms import UserCreationForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Email'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Confirm password'})

class ChallengeCreationForm(ModelForm):
    class Meta:
        model = Challenge
        fields = ['title', 'description', 'hours', 'color']
    def __init__(self, *args, **kwargs):
        super(ChallengeCreationForm, self).__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'id': 'descr'})
