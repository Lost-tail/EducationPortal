# Generated by Django 3.2 on 2021-05-12 08:28

from django.db import migrations, models
import internships.models
import internships.services.validators


class Migration(migrations.Migration):

    dependencies = [
        ('internships', '0007_alter_country_name'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='country',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='language',
            options={'ordering': ['name']},
        ),
        migrations.AlterField(
            model_name='company',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=internships.models.get_company_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Logo'),
        ),
        migrations.AlterField(
            model_name='internship',
            name='agreement',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_internship_application_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Agreement'),
        ),
        migrations.AlterField(
            model_name='internshipstudent',
            name='copy_agreement',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_internship_application_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Copy Agreement'),
        ),
        migrations.AlterField(
            model_name='student',
            name='identification',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Copy of Passport or ID"'),
        ),
        migrations.AlterField(
            model_name='student',
            name='language_certificate',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Language Certificate'),
        ),
        migrations.AlterField(
            model_name='student',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Photo'),
        ),
        migrations.AlterField(
            model_name='student',
            name='social_disadvantage_certificate',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Certificate Of Social Disadvantage'),
        ),
        migrations.AlterField(
            model_name='student',
            name='university_diploma',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='University Diploma'),
        ),
        migrations.AlterField(
            model_name='student',
            name='university_transcript_records',
            field=models.FileField(blank=True, null=True, upload_to=internships.models.get_student_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='University Transcript Records'),
        ),
        migrations.AlterField(
            model_name='university',
            name='logo',
            field=models.ImageField(blank=True, null=True, upload_to=internships.models.get_university_file_path, validators=[internships.services.validators.file_max_10mb_size], verbose_name='Logo'),
        ),
    ]