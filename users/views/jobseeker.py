from django.shortcuts import redirect, render, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import login
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from users.forms import JobseekerRegisterForm
from users.decorators import jobseeker_required


class JobseekerRegisterView(CreateView):
    model = get_user_model()
    form_class = JobseekerRegisterForm
    template_name = 'registration/jobseeker_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'jobseeker'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('home'))


@method_decorator([login_required, jobseeker_required], name='dispatch')
class JobSeekerDashboard(ListView):
    pass
