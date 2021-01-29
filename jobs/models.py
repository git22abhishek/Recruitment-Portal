from django.db import models
from users.models import Recruiter

# Create your models here.

class Job(models.Model):
    company = models.ForeignKey(Recruiter, on_delete=models.CASCADE)
    title = models.CharField(max_length=50)
    date_posted = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=1000)
    salary = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=30)

    def __str__(self):
        return f'{self.title}, at {self.company.username}'


