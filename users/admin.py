from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Category, Job, Recruiter, JobSeeker 

class UserAdmin(BaseUserAdmin):
    list_display=('username', 'email', 'date_joined', 'last_login', 'is_admin', 'is_recruiter', 'is_jobseeker', 'is_active')
    search_fields=('email', 'username')
    readonly_fields=('last_login', 'date_joined')
    filter_horizontal = ()
    list_filter=('last_login',)
    fieldsets=()

    add_fieldsets=(
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )

    ordering=('email',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}

class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'company', 'category', 'date_posted','country', 'city', 'vacancies')
    prepopulated_fields = {'slug': ('title',)}

# Register your models here.
admin.site.register(User, UserAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Job, JobAdmin)

