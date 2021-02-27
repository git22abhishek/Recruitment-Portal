from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.http import HttpResponse
from django.contrib.auth import (
    authenticate, login, logout
)
from ..forms import UserRegistrationForm, UserLoginForm


def home(request):
    if request.user.is_authenticated:
        if request.user.is_recruiter:
            return redirect('recruiter:recruiter_dashboard')
        else:
            return redirect(reverse('jobseeker_dashboard'))
    return render(request, 'home/homepage.html')


class Register(TemplateView):
    template_name = 'registration/register.html'


class AboutView(TemplateView):
    template_name = 'home/about.html'


def login_view(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserLoginForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user = authenticate(request, email=email,
                                password=password)

            if user != None:
                login(request, user)
                return redirect(reverse('home'))
                # request.user = user # everywhere on the page, unless
                # the user logouts or the session ends
            else:
                attempt = request.session.get("attempt") or 0
                request.session["attempt"] = attempt + 1
                request.session["invalid_user"] = 1  # 1 = True

    # if a GET (or any other method) create a blank form
    else:
        form = UserLoginForm()

    return render(request, 'registration/login.html', {"form": form})


def logout_view(request):
    logout(request)
    return redirect(reverse('home'))
