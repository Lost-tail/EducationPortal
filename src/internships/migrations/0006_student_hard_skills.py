# Generated by Django 3.2 on 2021-05-10 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0005_studenthardskill'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='hard_skills',
            field=models.ManyToManyField(blank=True, related_name='students', to='internships.StudentHardSkill'),
        ),
    ]
