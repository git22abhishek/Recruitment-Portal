from django import forms
from django.db import transaction
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import (
    authenticate,
    get_user_model
)

from .models import Job


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
                raise forms.ValidationError(
                    'The email or password in incorrect')
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
            raise forms.ValidationError(
                "No account exists with the given email")

        return email


class RecruiterRegisterForm(UserRegistrationForm):

    def __init__(self, *args, **kwargs):
        super(RecruiterRegisterForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {
            'placeholder': 'Company Name', }

    class Meta(UserRegistrationForm.Meta):
        model = get_user_model()
        # fields = ('email', 'username', 'password1', 'password2')
        # widgets = {
        #     'username': forms.TextInput(attrs={
        #         "placeholder": "Company Name"
        #     }),
        # }

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


class NewJobForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(NewJobForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs = {
            'placeholder': 'Job Title',
            'name': 'job[job-title]'
        }
        self.fields['category'].empty_label = 'Select Category'
        self.fields['work_location'].empty_label = 'Work Location'
        self.fields['category'].widget.attrs = {
            'class': 'ui fluid dropdown'
        }
        self.fields['vacancies'].widget.attrs = {
            'placeholder': 'Vacancies',
        }
        self.fields['last_date'].widget.attrs = {
            'id': 'last_date',
        }
        self.fields['last_date'].input_formats = ['%Y/%m/%d %H:%M']
        self.fields['salary'].widget.attrs = {
            'placeholder': 'Salary',
        }
        self.fields['country'].widget.attrs = {
            'placeholder': 'Country',
        }
        self.fields['city'].widget.attrs = {
            'placeholder': 'City',
        }
        self.fields['description'].widget.attrs = {
            'placeholder': 'Description',
        }

    class Meta:
        model = Job
        fields = (
            'title', 'category', 'description',
            'salary', 'vacancies', 'last_date',
            'country', 'city', 'work_location',
        )

    # title = forms.CharField(required=True,
    # widget=forms.TextInput(
    #     attrs={
    #         "placeholder": "Job Title"
    #     }
    # ))
