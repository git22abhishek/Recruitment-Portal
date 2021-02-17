from django.urls import path
from users.views import portal, recruiter, jobseeker

urlpatterns = [
    path('register/recruiter/', recruiter.RecruiterRegisterView.as_view(), name='recruiter_register'),
    path('register/jobseeker/', jobseeker.JobseekerRegisterView.as_view(), name='jobseeker_register'),
    path('register/', portal.Register.as_view(), name='register'),
    path('login/', portal.login_view, name='login'),
    path('logout/', portal.logout_view, name='logout'),
    path('', portal.home, name='home'),
]
