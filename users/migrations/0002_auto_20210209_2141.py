# Generated by Django 3.1.6 on 2021-02-09 16:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='is_job_seeker',
            new_name='is_jobseeker',
        ),
    ]