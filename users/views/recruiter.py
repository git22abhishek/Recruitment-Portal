from django.shortcuts import redirect, render, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from users.forms import RecruiterRegisterForm
from users.decorators import recruiter_required
from users.models import Job


class RecruiterRegisterView(CreateView):
    model = get_user_model()
    form_class = RecruiterRegisterForm
    template_name = 'registration/recruiter_register.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'recruiter'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(reverse('home'))

@method_decorator([login_required, recruiter_required], name='dispatch')
class RecruiterDashboard(ListView):
    model = get_user_model()
    # ordering = ('name', )
    # context_object_name = 'quizzes'

    def get_queryset(self):
        queryset = self.request.user.jobs
        return queryset

    template_name = 'home/recruiter_dashboard.html'

@method_decorator([login_required, recruiter_required], name='dispatch')
class CreateJobOpening(CreateView):
    model = Job
    fields = ('title', 'category', 'description', 'salary', 'location', 'vacancies',)
    template_name = 'recruiter/create_job_opening.html'

    def form_valid(self, form):
        job = form.save(commit=False)
        quiz.company = self.request.user
        quiz.save()
        messages.success(self.request, 'Job opening posted successfully!.')
        return redirect('recruiter:recruiter_dashboard', quiz.pk)




