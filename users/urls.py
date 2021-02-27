from django.urls import path, include
from users.views import portal, recruiter, jobseeker

urlpatterns = [
    path('about/', portal.AboutView.as_view(), name='about'),
    path('register/recruiter/', recruiter.RecruiterRegisterView.as_view(),
         name='recruiter_register'),
    path('register/jobseeker/', jobseeker.JobseekerRegisterView.as_view(),
         name='jobseeker_register'),
    path('register/', portal.Register.as_view(), name='register'),
    path('login/', portal.login_view, name='login'),
    path('logout/', portal.logout_view, name='logout'),
    # path('register/recruiter/', recruiter.RecruiterDashboard.as_view(), name='recruiter_dashboard'),
    path('', portal.home, name='home'),

    path('recruiter/', include(([
        path('create_job/', recruiter.CreateJobOpening.as_view(), name='create_job'),
        path('', recruiter.RecruiterDashboard.as_view(),
             name='recruiter_dashboard'),
    ], 'users'), namespace='recruiter'
    )),

    path('jobs/', include(([
        path('<slug:company>/<slug:slug>-<int:pk>/',
             recruiter.job_detail_view, name='job_details'),
        path('<slug:company>/<slug:slug>-<int:pk>/update/',
             recruiter.JobUpdateView.as_view(), name='update_job'),
    ], 'users'), namespace='jobs'
    )),
]
