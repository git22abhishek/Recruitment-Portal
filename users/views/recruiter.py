from django.shortcuts import redirect, render, reverse
from django.contrib.auth import get_user_model
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import (
    CreateView, DeleteView, DetailView, ListView, UpdateView
)
from users.forms import RecruiterRegisterForm
from users.decorators import recruiter_required


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
    pass
    # model = Quiz
    # ordering = ('name', )
    # context_object_name = 'quizzes'
    # template_name = 'classroom/teachers/quiz_change_list.html'

    # def get_queryset(self):
    #     queryset = self.request.user.quizzes \
    #         .select_related('subject') \
    #         .annotate(questions_count=Count('questions', distinct=True)) \
    #         .annotate(taken_count=Count('taken_quizzes', distinct=True))
    #     return queryset


