# Generated by Django 3.2 on 2021-05-19 10:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0011_alter_userconfirmation_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='userconfirmation',
            name='reseted',
            field=models.BooleanField(blank=True, default=False, null=True, verbose_name='Reseted'),
        ),
    ]
