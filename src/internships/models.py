from datetime import timedelta
import uuid

from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _

from .languages import LanguageField
from .services.validators import file_max_10mb_size


def get_student_file_path(instance, original_filename):
    ext = original_filename.split('.')[-1]
    updated_filename = f'{uuid.uuid4()}.{ext}'
    return f'students/{instance.id}/{updated_filename}'


def get_internship_application_file_path(instance, original_filename):
    ext = original_filename.split('.')[-1]
    updated_filename = f'{uuid.uuid4()}.{ext}'
    return f'internships_applications/{instance.id}/{updated_filename}'


def get_company_file_path(instance, original_filename):
    ext = original_filename.split('.')[-1]
    updated_filename = f'{uuid.uuid4()}.{ext}'
    return f'companies/{instance.id}/{updated_filename}'


def get_university_file_path(instance, original_filename):
    ext = original_filename.split('.')[-1]
    updated_filename = f'{uuid.uuid4()}.{ext}'
    return f'universities/{instance.id}/{updated_filename}'


class Country(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Country({self})'

    def __str__(self):
        return f'{self.name}'

    def get_admin_edit_url(self):
        return reverse('country_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('country_delete', args=[str(self.pk)])


class Language(models.Model):
    name = models.CharField('Name', max_length=64, unique=True)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'Language({self})'

    def __str__(self):
        return f'{self.name}'


    def get_student_remove_url(self):
        return reverse('student_language_remove', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('language_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('language_delete', args=[str(self.pk)])


class ContactPerson(models.Model):
    name = models.CharField('Name', max_length=2048)
    email = models.EmailField('Email', max_length=2048)
    phone = models.CharField('Phone', max_length=2048, null=True, blank=True)

    def __repr__(self):
        return f'ContactPerson({self})'

    def __str__(self):
        return f'{self.name}, {self.email}'


class Student(models.Model):
    class Genders(models.TextChoices):
        MALE = ('MALE', _('Male'))
        FEMALE = ('FEMALE', _('Female'))

    activated = models.BooleanField('Activated', null=True, blank=True, default=False)
    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    full_name = models.CharField('Full Name', max_length=2048, null=True, blank=True, default='')
    gender = models.CharField(
        'Gender', 
        max_length=32, 
        choices=Genders.choices,
        blank=True,
        null=True, 
        default=''
    )
    birthdate = models.DateField('Birthdate', null=True, blank=True)
    contact_phone = models.CharField('Contact Phone', max_length=64, null=True, blank=True, default='')
    country = models.ForeignKey(
        Country,
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='students'
    )
    city = models.CharField('City', max_length=2048, null=True, blank=True, default='')
    main_cv = models.TextField('Main CV', null=True, blank=True, default='')
    soft_skills = models.ManyToManyField('StudentSoftSkill', related_name='students', blank=True)
    hard_skills = models.ManyToManyField('StudentHardSkill', related_name='students', blank=True)
    languages = models.ManyToManyField(Language, related_name='students', blank=True)
    facebook = models.TextField('Facebook', null=True, blank=True, default='')
    twitter = models.TextField('Twitter', null=True, blank=True, default='')
    linkedin = models.TextField('LinkedIn', null=True, blank=True, default='')
    instagram = models.TextField('Instagram', null=True, blank=True, default='')
    card_number = models.CharField('StudentCardNumber', max_length=2048, null=True, blank=True, default='')

    university = models.ForeignKey(
        'University', 
        null=True, 
        blank=True, 
        default=None, 
        on_delete=models.SET_NULL
    )
    university_name = models.TextField('University Name', null=True, blank=True, default='')
    university_email = models.EmailField(
        'University Email', max_length=2048, null=True, blank=True, default=''
    )
    confirmed = models.BooleanField('Confirmed', null=True, blank=True, default=False)

    academic_merit = models.IntegerField('Academic merit', null=True, blank=True, default=None)
    research_experience = models.IntegerField('Research experience', null=True, blank=True, default=None)
    motivation = models.IntegerField('Motivation', null=True, blank=True, default=None)
    language_skill = models.IntegerField('Language skill', null=True, blank=True, default=None)
    overall = models.IntegerField('Overall assessment', null=True, blank=True, default=None)
    
    photo = models.ImageField(
        'Photo', 
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )
    identification = models.FileField(
        'Copy of Passport or ID"',
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )
    university_transcript_records = models.FileField(
        'University Transcript Records',
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )
    language_certificate = models.FileField(
        'Language Certificate',
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )
    university_diploma = models.FileField(
        'University Diploma',
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )
    social_disadvantage_certificate = models.FileField(
        'Certificate Of Social Disadvantage',
        upload_to=get_student_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'Student({self})'

    def __str__(self):
        return f'{self.full_name}, {self.user.email}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            
            super(self.__class__, self).save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

        super(self.__class__, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('student_detail', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('student_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('student_delete', args=[str(self.pk)])

    @property
    def age(self):
        return int((timezone.now().date() - self.birthdate).days / 365.25)



class StudentSoftSkill(models.Model):
    name = models.CharField('Name', max_length=2048)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'StudentSoftSkill({self})'

    def __str__(self):
        return f'{self.name}'


class StudentHardSkill(models.Model):
    name = models.CharField('Name', max_length=2048)

    class Meta:
        ordering = ['name']

    def __repr__(self):
        return f'StudentHardSkill({self})'

    def __str__(self):
        return f'{self.name}'


class StudentEducation(models.Model):
    university_name = models.CharField('University Name', max_length=2048)
    locality = models.CharField('Locality', max_length=2048)
    start_year = models.IntegerField('Start Year')
    finish_year = models.IntegerField('Finish Year')
    study_cycle = models.CharField(
        'Study Cycle', 
        max_length=32, 
        choices=[('bachelor', 'bachelor'), ('master', 'master'), ('PhD', 'PhD')]
    )
    degree_program = models.CharField('Degree Program', max_length=2048)
    description = models.TextField('Description', default='')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='education'
    )

    class Meta:
        ordering = ['-finish_year', '-start_year']

    def __repr__(self):
        return f'StudentEducation({self})'

    def __str__(self):
        return f'{self.university_name}, {self.study_cycle}'

    def get_edit_url(self):
        return reverse('student_education_edit', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('student_education_delete', args=[str(self.pk)])


class StudentEducationAcquiredSkill(models.Model):
    """Principal subject covered or skill acquired"""
    name = models.CharField('Name', max_length=2048)

    def __repr__(self):
        return f'StudentEducationAcquiredSkill({self})'

    def __str__(self):
        return f'{self.name}'


class StudentWork(models.Model):
    company_name = models.CharField('Company Name', max_length=2048)
    locality = models.CharField('Locality', max_length=2048)
    start_year = models.IntegerField('Start Year',)
    finish_year = models.IntegerField('Finish Year')
    position_held = models.CharField('Position Held', max_length=2048)
    description = models.TextField('Description', default='')
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='work'
    )

    class Meta:
        ordering = ['-finish_year', '-start_year']

    def __repr__(self):
        return f'StudentWork({self})'

    def __str__(self):
        return f'{self.company_name}, {self.position_held}'

    def get_edit_url(self):
        return reverse('student_work_edit', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('student_work_delete', args=[str(self.pk)])


class StudentWorkResponsibility(models.Model):
    """Main activity or responsibility"""
    name = models.CharField('Name', max_length=2048)

    def __repr__(self):
        return f'StudentWorkResponsibility({self})'

    def __str__(self):
        return f'{self.name}'


class StudentPublication(models.Model):
    title = models.CharField('Title', max_length=2048)
    year = models.IntegerField('Year')
    author = models.CharField('Author', max_length=2048)
    publisher = models.CharField('Publisher', max_length=2048)
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='publications'
    )

    class Meta:
        ordering = ['-year']

    def __repr__(self):
        return f'StudentPublication({self})'

    def __str__(self):
        return f'{self.title}, {self.publisher}'

    def get_edit_url(self):
        return reverse('student_publication_edit', args=[str(self.pk)])

    def get_delete_url(self):
        return reverse('student_publication_delete', args=[str(self.pk)])


class University(models.Model):
    activated = models.BooleanField('Activated', null=True, blank=True, default=False)
    user = models.OneToOneField(User, related_name='university', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Name', max_length=2048, null=True, blank=True, default='', unique=True)
    country = models.ForeignKey(
        Country, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='universities'
    )
    address = models.CharField('Address', max_length=2048, null=True, blank=True, default='')
    description = models.TextField('Description', null=True, blank=True, default='')
    about_department = models.TextField('About Department', null=True, blank=True, default='')
    year_estabilished = models.IntegerField('Year Estabilished', null=True, blank=True)
    number_of_students = models.IntegerField(
        'Number Of Students', 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0)]
    )
    phone = models.CharField('Phone', max_length=2048, null=True, blank=True, default='')
    website = models.TextField('Website', null=True, blank=True, default='')
    email = models.EmailField('Contact Email', max_length=2048, null=True, blank=True, default='')
    contact_person = models.ForeignKey(
        ContactPerson, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='universitis'
    )
    affiliated_companies = models.ManyToManyField(
        'Company', 
        related_name='affiliated_universities', 
        blank=True
    )
    logo = models.ImageField(
        'Logo',
        upload_to=get_university_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'University({self})'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            
            super(self.__class__, self).save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

        super(self.__class__, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('university_detail', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('university_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('university_delete', args=[str(self.pk)])

    @property
    def get_active_internships(self):
        return self.internships.filter(activated=True, status='CALL')


class Company(models.Model):
    activated = models.BooleanField('Activated', null=True, blank=True, default=False)
    user = models.OneToOneField(User, related_name='company', on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Name', max_length=2048, null=True, blank=True, default='', unique=True)
    country = models.ForeignKey(
        Country, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='comanies'
    )
    address = models.CharField('Address', max_length=2048, null=True, blank=True, default='')
    description = models.TextField('Description', null=True, blank=True, default='')
    professional_sphere = models.TextField('Professional Sphere', null=True, blank=True, default='')
    year_estabilished = models.IntegerField('Year Estabilished', null=True, blank=True)
    number_of_employees = models.IntegerField(
        'Number Of Employees', 
        null=True, 
        blank=True, 
        validators=[MinValueValidator(0)]
    )
    phone = models.CharField('Phone', max_length=2048, null=True, blank=True, default='')
    website = models.TextField('Website', null=True, blank=True, default='')
    email = models.EmailField('Contact Email', max_length=2048, null=True, blank=True, default='')
    contact_person = models.ForeignKey(
        ContactPerson, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='companies'
    )
    logo = models.ImageField(
        'Logo',
        upload_to=get_company_file_path,
        null=True,
        blank=True,
        validators=[file_max_10mb_size]
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'Company({self})'

    def __str__(self):
        return f'{self.name}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            
            super(self.__class__, self).save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

        super(self.__class__, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('company_detail', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('company_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('company_delete', args=[str(self.pk)])

    @property
    def get_active_internships(self):
        return self.internships.filter(activated=True, status='CALL')


class Internship(models.Model):
    class Statuses(models.TextChoices):
        CALL = ('CALL', _('CALL'))
        ENROLL = ('ENROLL', _('ENROLL'))
        INTERNSHIP = ('INTERNSHIP', _('INTERNSHIP'))
        CLOSE = ('CLOSE', _('CLOSE'))

    activated = models.BooleanField('Activated', null=True, blank=True, default=True)
    created = models.DateTimeField(auto_now_add=True)

    name = models.CharField('Name', max_length=2048)
    start_date = models.DateField('Start Date')
    end_date = models.DateField('End Date')
    applications_deadline = models.DateField('Appications Deadline')
    seats_number = models.IntegerField('Number of Students (Max.)', validators=[MinValueValidator(1)])
    description = models.TextField('Description')
    required_knowledge = models.TextField('Required Knowledges and Skills', null=True, blank=True)
    objectives = models.TextField('Objectives', null=True, blank=True)
    short_course_modules = models.TextField('Short Course Modules', null=True, blank=True, default='')
    additional_notes = models.TextField('Additional Notes', null=True, blank=True, default='')
    country = models.ForeignKey(
        Country,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='internships'
    )
    university = models.ForeignKey(University, on_delete=models.CASCADE, related_name='internships')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='internships')
    status = models.CharField(
        'Status',
        max_length=64,
        null=True,
        blank=True,
        choices=Statuses.choices,
        default=Statuses.CALL
    )
    academic_coordinator = models.OneToOneField(
        ContactPerson, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='university_for_academic_coordinator'
    )
    academic_tutor = models.OneToOneField(
        ContactPerson, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='university_for_academic_tutor'
    )
    hosting_institution_tutor = models.OneToOneField(
        ContactPerson, 
        null=True, 
        blank=True, 
        on_delete=models.SET_NULL,
        related_name='university_for_host_tutor'
    )
    agreement = models.FileField(
        'Agreement',
        null=True,
        blank=True,
        upload_to=get_internship_application_file_path,
        validators=[file_max_10mb_size]
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'Internship({self})'

    def __str__(self):
        return f'{self.name}, {self.university}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            
            super(self.__class__, self).save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

        super(self.__class__, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('internship_detail', args=[str(self.pk)])

    def get_apply_url(self):
        return reverse('internship_apply', args=[str(self.pk)])

    def get_edit_url(self):
        return reverse('internship_edit', args=[str(self.pk)])

    def get_applications_url(self):
        return reverse('internship_applications', args=[str(self.pk)])

    def get_interns_url(self):
        return reverse('internship_interns', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('internship_delete', args=[str(self.pk)])

    def get_admin_applications_url(self):
        return reverse('internship_applications_list', args=[str(self.pk)])

    def get_admin_interns_url(self):
        return reverse('internship_interns_list', args=[str(self.pk)])
    
    @property
    def is_applying(self):
        if not self.number_of_free_positions or self.status != 'CALL'\
                or (self.applications_deadline and timezone.now().date() > self.applications_deadline):
            return False
        return True

    @property
    def number_of_free_positions(self):
        number = self.seats_number - self.interns.count()
        if number <= 0:
            return 0
        return number

    @property
    def days_before_deadline(self):
        return timedelta(days=self.applications_deadline.day - timezone.now().day)

    @property
    def get_new_applications_count(self):
        return self.applications.filter(status='CONSIDERED').count()


class InternshipStudent(models.Model):
    created = models.DateTimeField(auto_now_add=True)

    internship = models.ForeignKey(Internship, on_delete=models.CASCADE, related_name='interns')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='interns')
    application = models.OneToOneField('InternshipApplication', on_delete=models.CASCADE, related_name='intern')
    copy_agreement = models.FileField(
        'Copy Agreement',
        null=True,
        blank=True,
        upload_to=get_internship_application_file_path,
        validators=[file_max_10mb_size]
    )
    review = models.OneToOneField(
        'InternshipReview', 
        null=True, 
        blank=True, 
        default=None,
        on_delete=models.SET_NULL,
        related_name='review'
    )
    university_review = models.OneToOneField(
        'InternshipReview', 
        null=True, 
        blank=True, 
        default=None,
        on_delete=models.SET_NULL,
        related_name='university_review'
    )
    company_review = models.OneToOneField(
        'InternshipReview', 
        null=True, 
        blank=True, 
        default=None,
        on_delete=models.SET_NULL,
        related_name='company_review'
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'InternshipStudent({self})'

    def __str__(self):
        return f'{self.student}, {self.internship}'

    def get_add_review_url(self):
        return reverse('internship_student_add_review', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('internship_student_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('internship_student_delete', args=[str(self.pk)])


class InternshipStatus(models.Model):
    name = models.CharField('Name', max_length=64)

    def __repr__(self):
        return f'InternshipStatus({self})'

    def __str__(self):
        return f'{self.name}'


class InternshipReview(models.Model):
    activated = models.BooleanField('Activated', null=True, blank=True, default=False)
    created = models.DateTimeField(auto_now_add=True)

    text = models.TextField('Text Review', null=True, default=True)

    def __repr__(self):
        return f'InternshipReview({self})'

    def __str__(self):
        return f'{self.text}'


class InternshipApplication(models.Model):
    class Statuses(models.TextChoices):
        CONSIDERED = ('CONSIDERED', _('CONSIDERED'))
        APPROVED = ('APPROVED', _('APPROVED'))
        REJECTED = ('REJECTED', _('REJECTED'))

    created = models.DateTimeField(auto_now_add=True)

    cover_letter = models.TextField('Cover Letter')
    internship = models.ForeignKey(
        Internship, 
        on_delete=models.CASCADE,
        related_name='applications'
    )
    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name='internships_applications'
    )
    university_assessment = models.FloatField(
        'University Assessment',
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(10)],
        default=0
    )
    status = models.CharField(
        'Status',
        max_length=64,
        null=True,
        blank=True,
        choices=Statuses.choices,
        default=Statuses.CONSIDERED
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'InternshipApplication({self})'

    def __str__(self):
        return f'{self.status}, {self.internship}, {self.student}'

    def save(self, *args, **kwargs):
        if self.id is None:
            saved = []
            for f in self.__class__._meta.get_fields():
                if isinstance(f, models.FileField):
                    saved.append((f.name, getattr(self, f.name)))
                    setattr(self, f.name, None)
            
            super(self.__class__, self).save(*args, **kwargs)

            for name, val in saved:
                setattr(self, name, val)

        super(self.__class__, self).save(*args, **kwargs)

    def get_detail_url(self):
        return reverse('internship_application_detail', args=[str(self.internship.pk), str(self.pk)])

    def get_approve_url(self):
        return reverse('internship_application_approve', args=[str(self.internship.pk), str(self.pk)])

    def get_reject_url(self):
        return reverse('internship_application_reject', args=[str(self.internship.pk), str(self.pk)])

    def get_student_detail_url(self):
        return reverse('student_internship_application_detail', args=[str(self.pk)])

    def get_admin_edit_url(self):
        return reverse('internship_application_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('internship_application_delete', args=[str(self.pk)])


class StaffUser(models.Model):
    STAFF_TYPES = [
        ('SuperAdmin', 'SuperAdmin'),
        ('University Representative', 'University Representative'),
        ('Company Representative', 'Company Representative')
    ]

    created = models.DateTimeField('Created', auto_now_add=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_user')
    
    full_name = models.CharField('Full Name', max_length=2048, null=True)
    staff_type = models.CharField('Type', max_length=64, choices=STAFF_TYPES)
    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='staff_users'
    )
    university = models.ForeignKey(
        University,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='staff_users'
    )

    class Meta:
        ordering = ['-id']

    def __repr__(self):
        return f'StaffUser({self})'

    def __str__(self):
        return f'{self.user.email}, {self.staff_type}'

    def get_admin_edit_url(self):
        return reverse('staff_user_edit', args=[str(self.pk)])

    def get_admin_delete_url(self):
        return reverse('staff_user_delete', args=[str(self.pk)])


class UserConfirmation(models.Model):
    USER_TYPES = [
        ('student', 'student'),
        ('university', 'university'),
        ('company', 'company'),
        ('University Representative', 'University Representative'),
        ('Company Representative', 'Company Representative'),
        ('SuperAdmin', 'SuperAdmin')
    ]
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField('Created', auto_now_add=True)
    updated = models.DateTimeField('Updated', auto_now=True)
    reseted = models.BooleanField('Reseted', null=True, blank=True, default=False)
    user = models.OneToOneField(
        User, 
        related_name='confirmation',
        blank=True,
        null=True,
        on_delete=models.CASCADE
    )
    name = models.CharField('Name', max_length=2048)
    email = models.EmailField('Email', max_length=2048)
    password = models.TextField('Password')
    token = models.TextField('Token', unique=True, blank=True, null=True)
    user_type = models.CharField('User Type', max_length=126, choices=USER_TYPES)
    card_number = models.CharField('StudentCardNumber', max_length=2048, null=True, blank=True, default='')
    company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='confirmations'
    )
    university = models.ForeignKey(
        University,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='confirmations'
    )

    def __repr__(self):
        return f'StudentConfirmation({self})'

    def __str__(self):
        return f'{self.email}, {self.name}'

    def get_signup_confirm_email_url(self):
        return reverse('signup_confirm_email', args=[str(self.pk), self.token])

    def get_signup_confirm_representative_url(self):
        return reverse('signup_confirm_representative', args=[str(self.pk), self.token])

    def get_reset_password_url(self):
        return reverse('reset_password', args=[str(self.pk), self.token])


class InternshipFile(models.Model):
    file = models.FileField(
        'File',
        null=True,
        blank=True,
        upload_to=get_internship_application_file_path,
        validators=[file_max_10mb_size]
    )
    review = models.ForeignKey(
        InternshipReview,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name='files'
    )