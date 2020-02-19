# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Player

class PlayerCreationForm(UserCreationForm):

    class Meta:
        model = Player
        fields = ('username', 'email')

class PlayerChangeForm(UserChangeForm):

    class Meta:
        model = Player
        fields = ('username', 'email')