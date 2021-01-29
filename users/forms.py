from django import forms
from . models import User
from django.contrib.auth import (
    authenticate,
    get_user_model
 )

# class UserCreationForm(forms.ModelForm):
    
#     class Meta:
#         model = User
#         fields = ('email', 'username', 'password')


class UserLoginForm(forms.Form):
    email = forms.EmailField( required=True)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('The user does not exist')
            if not user.check_password(password):
                raise forms.ValidationError('The email or password is incorrect')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')
        
        return super(UserLoginForm, self).clean(*args, **kwargs) 


class UserRegisterForm(forms.ModelForm):
    pass