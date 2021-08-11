# Generated by Django 3.2 on 2021-05-28 16:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0013_auto_20210526_1910'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='internshipreview',
            name='internship',
        ),
        migrations.RemoveField(
            model_name='internshipreview',
            name='student',
        ),
        migrations.RemoveField(
            model_name='internshipreview',
            name='student_review',
        ),
        migrations.RemoveField(
            model_name='internshipreview',
            name='university_review',
        ),
        migrations.AddField(
            model_name='internshipreview',
            name='activated',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Activated'),
        ),
        migrations.AddField(
            model_name='internshipreview',
            name='text',
            field=models.TextField(default=True, null=True, verbose_name='Text Review'),
        ),
        migrations.AddField(
            model_name='internshipstudent',
            name='company_review',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='company_review', to='internships.internshipreview'),
        ),
        migrations.AddField(
            model_name='internshipstudent',
            name='review',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='review', to='internships.internshipreview'),
        ),
        migrations.AddField(
            model_name='internshipstudent',
            name='university_review',
            field=models.OneToOneField(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='university_review', to='internships.internshipreview'),
        ),
    ]