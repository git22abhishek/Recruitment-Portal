from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.shortcuts import reverse



# Manager for custom user model
class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("Email is a required field")
        if not username:
            raise ValueError("Username is a required field")

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=email,
            username=username,
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser= True
        
        user.save(using=self._db)
        return user


#Custom user model
class User(AbstractBaseUser):
    email = models.EmailField(verbose_name="Email address", max_length=60, unique=True)
    username = models.CharField(verbose_name="Username", max_length=30)
    date_joined = models.DateTimeField(verbose_name="date joined", auto_now_add=True)
    last_login = models.DateTimeField(verbose_name="last login", auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    
    is_recruiter = models.BooleanField(default=False)
    is_jobseeker = models.BooleanField(default=False)

    # This is the field that the user should login with
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return f'{self.username}, {self.email}'

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    def get_absolute_url(self):
        return "/users/%i/" % (self.pk)

    def get_email(self):
        return self.email


class Recruiter(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class JobSeeker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class Category(models.Model):
    name = models.CharField(max_length=30, db_index=True)
    slug = models.SlugField(max_length=30, unique=True)

    class Meta:
        verbose_name_plural = 'categories'

    def get_absolute_url(self):
        # return reverse("category_list", kwargs={"pk": self.pk})
        return reverse("category_list", args=[self.slug])
    
    def __str__(self):
        return self.name

class Job(models.Model):
    company = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name='jobs')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=30, unique=True)
    date_posted = models.DateTimeField(auto_now_add=True)
    description = models.TextField()
    salary = models.PositiveIntegerField(null=True)
    location = models.CharField(max_length=30)
    vacancies = models.IntegerField(default=1)

    class Meta:
        ordering = ('-date_posted',)

    def __str__(self):
        return f'{self.title}, at {self.company.username}'

            
