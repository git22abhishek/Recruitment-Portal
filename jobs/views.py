from django.shortcuts import render
from .models import Job

# Create your views here.
def JobList(request):
    jobs = Job.objects.all()
    context = { 'title': 'All Jobs', 'jobs': jobs }
    return render(request, 'jobs/joblist.html',context=context)