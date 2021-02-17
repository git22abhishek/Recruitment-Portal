from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model
 )

class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', 'password1', 'password2')

    email = forms.EmailField(required=True,
    widget=forms.TextInput(
        attrs={
            "placeholder": "E-mail address"
        }
    ))
    username = forms.CharField(required=True, 
    widget=forms.TextInput(
        attrs={
            "placeholder": "Username"
        }
    )) 
    password1 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "password"
        }
    ))
    password2 = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "confirm password"
        }
    ))

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        qs = User.objects.filter(email__iexact=email)

        if qs.exists():
            raise forms.ValidationError("Email already in use") 

        return email

    def clean_username(self, *args, **kwargs):
        return self.cleaned_data.get('username')

    def save(self, *args, **kwargs):
        if self.clean_email():
            user = super().save(commit=False)
            return user

        

class UserLoginForm(forms.Form):
    email = forms.EmailField(required=True, 
    widget=forms.TextInput(
        attrs={
            "placeholder": "E-mail address"
        }
    ))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            "placeholder": "password"
        }
    ))

    def clean(self, *args, **kwargs):
        email = self.clean_email()
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('The email or password in incorrect')
            # if not user.check_password(password):
            #     raise forms.ValidationError('The email or password is incorrect')
            if not user.is_active:
                raise forms.ValidationError('This user is not active')

        return super(UserLoginForm, self).clean(*args, **kwargs)

    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        User = get_user_model()
        qs = User.objects.filter(email__iexact=email)

        if not qs.exists():
            raise forms.ValidationError("No account exists with the given email") 

        return email

class RecruiterRegisterForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = get_user_model()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_recruiter = True
        if commit:
            user.save()
        return user

class JobseekerRegisterForm(UserRegistrationForm):
    class Meta(UserRegistrationForm.Meta):
        model = get_user_model()

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_jobseeker = True
        if commit:
            user.save()
        return user