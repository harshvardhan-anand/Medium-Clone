from django import forms
from django.contrib.auth.models import User
from .models import Profile


class CreateUserForm(forms.ModelForm):
    password1 = forms.CharField(
        widget = forms.PasswordInput,max_length=50, label='Password'
    )    
    password2 = forms.CharField(
        widget = forms.PasswordInput,max_length=50, label='Retype Password'
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd.get('password2')!=cd.get('password1'):
            raise forms.ValidationError("Password didn't matched")
        return cd.get('password2')