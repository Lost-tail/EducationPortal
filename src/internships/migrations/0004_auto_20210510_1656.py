# Generated by Django 3.2 on 2021-05-10 16:56

from django.db import migrations, models
import internships.models


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0003_auto_20210509_1633'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='internshipstudent',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='studenteducation',
            options={'ordering': ['-finish_year', '-start_year']},
        ),
        migrations.AlterModelOptions(
            name='studentwork',
            options={'ordering': ['-finish_year', '-start_year']},
        ),
        migrations.AlterField(
            model_name='company',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=2048, null=True, verbose_name='Contact Email'),
        ),
        migrations.AlterField(
            model_name='student',
            name='identification',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, verbose_name='Copy of Passport or ID"'),
        ),
        migrations.AlterField(
            model_name='student',
            name='university_diploma',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, verbose_name='University Diploma'),
        ),
        migrations.AlterField(
            model_name='studenteducation',
            name='finish_year',
            field=models.IntegerField(verbose_name='Finish Year'),
        ),
        migrations.AlterField(
            model_name='studenteducation',
            name='start_year',
            field=models.IntegerField(verbose_name='Start Year'),
        ),
        migrations.AlterField(
            model_name='studentpublication',
            name='year',
            field=models.IntegerField(verbose_name='Year'),
        ),
        migrations.AlterField(
            model_name='studentwork',
            name='finish_year',
            field=models.IntegerField(verbose_name='Finish Year'),
        ),
        migrations.AlterField(
            model_name='studentwork',
            name='start_year',
            field=models.IntegerField(verbose_name='Start Year'),
        ),
        migrations.AlterField(
            model_name='university',
            name='email',
            field=models.EmailField(blank=True, default='', max_length=2048, null=True, verbose_name='Contact Email'),
        ),
    ]