# Generated by Django 3.2 on 2021-05-29 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0016_auto_20210529_0821'),
    ]

    operations = [
        migrations.AddField(
            model_name='student',
            name='university_name',
            field=models.TextField(blank=True, default='', null=True, verbose_name='University Name'),
        ),
    ]
