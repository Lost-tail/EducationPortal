from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.utils.translation import gettext as _

from .models import (
    Company, Country, ContactPerson, InternshipApplication, InternshipStudent, InternshipFile,
    Internship, Language, StaffUser, Student, StudentEducation, StudentWork, StudentPublication, University
)
from .services.services import get_object_or_none, user_email_already_exist
from .services.validators import (
    clean_internship_applications_deadline, clean_internship_start_date
)


class StudentForm(forms.ModelForm):
    birthdate = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=False
    )
    
    class Meta:
        model = Student
        exclude = ['created', 'user', 'activated', 'soft_skills', 'languages']


class StudentEducationForm(forms.ModelForm):
    class Meta:
        model = StudentEducation
        exclude = ['student']


class StudentWorkForm(forms.ModelForm):
    class Meta:
        model = StudentWork
        exclude = ['student']


class StudentPublicationForm(forms.ModelForm):
    class Meta:
        model = StudentPublication
        exclude = ['student']


class RegisterStudentForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048)
    password = forms.CharField(max_length=4096)
    card_number = forms.CharField(max_length=2048)
    university = forms.ModelChoiceField(queryset=University.objects.all())

    class Meta:
        model = Student
        fields = ['full_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if user_email_already_exist(email):
            raise ValidationError(_('This email is already taken'))
        return email


class StudentProfileForm(forms.ModelForm):
    birthdate = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=False
    )
    
    class Meta:
        model = Student
        fields = ['full_name', 'gender', 'birthdate', 'city', 'country']


class StudentPhotoForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['photo']


class StudentMainCVForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['main_cv']


class StudentSocialNetworksForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['facebook', 'twitter', 'linkedin', 'instagram']


class StudentFilesForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = [
            'identification', 
            'university_transcript_records', 
            'language_certificate',
            'university_diploma',
            'social_disadvantage_certificate'
        ]



class InternshipForm(forms.ModelForm):
    activated = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, True), (None, False)]),
        required=False
    )
    applications_deadline = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=True
    )
    start_date = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=True
    )
    end_date = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=True
    )

    class Meta:
        model = Internship
        exclude = [
            'created', 'university', 'status', 
            'academic_coordinator', 'academic_tutor', 'hosting_institution_tutor'
        ]

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'country': instance.country,
                'company': instance.company,
                'university': instance.university
            })
            kwargs.update({'initial': initial})
        return super(InternshipForm, self).__init__(*args, **kwargs)

    def clean(self, *args, **kwargs):
        cleaned_data = super(InternshipForm, self).clean(*args, **kwargs)
        clean_internship_applications_deadline(self)
        clean_internship_start_date(self)
        return cleaned_data


    # def clean_start_date(self):
    #     # print(self.clean_end_date())
    #     # print(self.cleaned_data)
    #     return clean_internship_start_date(self.cleaned_data)

    # def clean_end_date(self):
    #     print(self.cleaned_data)
    #     return self.cleaned_data['end_date']

    # def clean_end_date(self):
    #     print(self.cleaned_data)
    #     return self.cleaned_data['end_date']
        

class InternshipStudentForm(forms.ModelForm):
    class Meta:
        model = InternshipStudent
        exclude = ['internship', 'created', 'student', 'application']


class UniversityForm(forms.ModelForm):
    activated = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, 'on'), (False, None)]),
        required=False
    )

    class Meta:
        model = University
        exclude = ['user', 'created', 'activated']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'country': instance.country,
                'user': instance.user,
                'contact_person': instance.contact_person
            })
            kwargs.update({'initial': initial})
        return super(UniversityForm, self).__init__(*args, **kwargs)


class RegisterUniversityForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048)
    password = forms.CharField(max_length=4096)

    class Meta:
        model = University
        fields = ['name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_object_or_none(User, email=email):
            raise ValidationError(_('This email is already taken'))
        return email


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        exclude = ['user', 'created', 'activated']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'country': instance.country,
                'user': instance.user,
                'contact_person': instance.contact_person
            })
            kwargs.update({'initial': initial})
        return super(CompanyForm, self).__init__(*args, **kwargs)


class RegisterCompanyForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048)
    password = forms.CharField(max_length=4096)

    class Meta:
        model = Company
        fields = ['name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_object_or_none(User, email=email):
            raise ValidationError(_('This email is already taken'))
        return email


class ContactPersonForm(forms.ModelForm):
    class Meta:
        model = ContactPerson
        fields = '__all__'


class CountryForm(forms.ModelForm):
    class Meta:
        model = Country
        fields = '__all__'


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = '__all__'


class InternshipApplicationForm(forms.ModelForm):
    class Meta:
        model = InternshipApplication
        exclude = ['created']


class StaffUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048)

    class Meta:
        model = StaffUser
        exclude = ['created', 'user', 'staff_type']

    def clean_email(self):
        email = self.cleaned_data['email']
        if not (self.instance and self.instance.user.email == email)\
                and user_email_already_exist(email):
            raise ValidationError(_('This email is already taken'))
        return email


class RegisterStaffUserForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048)
    password = forms.CharField(max_length=4096) 

    class Meta:
        model = StaffUser
        exclude = ['created', 'user']

    def clean_email(self):
        email = self.cleaned_data['email']
        if user_email_already_exist(email):
            raise ValidationError(_('This email is already taken'))
        return email


class AddRepresentativeForm(forms.ModelForm):
    email = forms.EmailField(max_length=2048, required=True)

    class Meta:
        model = StaffUser
        fields = ['full_name']

    def clean_email(self):
        email = self.cleaned_data['email']
        if user_email_already_exist(email):
            raise ValidationError(_('This email is already taken'))
        return email


class InternshipFileForm(forms.ModelForm):
    class Meta:
        model = InternshipFile
        fields = ['file']