from django.shortcuts import (
    redirect, render, reverse, get_object_or_404
)
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.template.defaultfilters import slugify

from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from users.forms import RecruiterRegisterForm, NewJobForm
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
    model = Job
    # ordering = ('name', )
    # context_object_name = 'quizzes'

    # def get_queryset(self):
    #     queryset = self.request.user.jobs
    #     return queryset

    template_name = 'home/recruiter_dashboard.html'


@method_decorator([login_required, recruiter_required], name='dispatch')
class CreateJobOpening(CreateView):
    model = Job
    form_class = NewJobForm
    template_name = 'recruiter/create_job_opening.html'

    def form_valid(self, form):
        # this hasn't yet saved to the database.
        job = form.save(commit=False)
        job.slug = slugify(job.title)
        job.company = self.request.user
        job.save()
        messages.success(self.request, 'Job opening posted successfully!')
        # Save again - this time to the database
        return super().form_valid(form)
        # return redirect('recruiter:recruiter_dashboard', job.slug)


@method_decorator([login_required], name='dispatch')
class JobDetailView(DetailView):
    model = Job
    template_name = 'home/job_details.html'

    def get_object(self):
        return get_object_or_404(Job,
                                 id=self.kwargs['pk'],
                                 slug=self.kwargs['slug'],
                                 company__slug=self.kwargs['company']
                                 )


@method_decorator([login_required, recruiter_required], name='dispatch')
class JobUpdateView(UpdateView):
    model = Job
    template_name = 'recruiter/update_job.html'

    def get_object(self):
        return get_object_or_404(Job,
                                 id=self.kwargs['pk'],
                                 company__username=self.kwargs['company'],
                                 company=self.request.user
                                 )

    def form_valid(self, form):
        # Update the slug if the title has changed.
        job = form.save(commit=False)
        job.slug = slugify(job.title)
        job.save()
        return super().form_valid(form)
