from django import forms
from django.utils.translation import ugettext_lazy as _

from internships.models import (
    ContactPerson, Company, Internship, InternshipApplication, 
    InternshipStudent, Student, University
)


class StudentAdminForm(forms.ModelForm):
    birthdate = forms.DateField(
        input_formats=['%d/%m/%Y'], 
        widget=forms.DateInput(format='%d/%m/%Y'),
        required=False
    )
    
    class Meta:
        model = Student
        exclude = ['created', 'user', 'soft_skills', 'languages']


class UniversityAdminForm(forms.ModelForm):
    activated = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, 'on'), (False, None)]),
        required=False
    )

    class Meta:
        model = University
        exclude = ['user', 'created']

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
        return super(UniversityAdminForm, self).__init__(*args, **kwargs)


class CompanyAdminForm(forms.ModelForm):
    activated = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, 'on'), (False, None)]),
        required=False
    )

    class Meta:
        model = Company
        exclude = ['user', 'created']

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
        return super(CompanyAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        return super(CompanyAdminForm, self).save(commit)



class InternshipAdminForm(forms.ModelForm):
    activated = forms.BooleanField(
        widget=forms.RadioSelect(choices=[(True, 'on'), (False, None)]),
        required=False
    )
    status = forms.ChoiceField(choices=Internship.Statuses.choices)


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

    academic_coordinator_name = forms.CharField(
        max_length=2048,
        required=True
    )
    academic_coordinator_email = forms.EmailField(
        max_length=2048,
        required=True
    )
    academic_tutor_name = forms.CharField(
        max_length=2048,
        required=True
    )
    academic_tutor_email = forms.EmailField(
        max_length=2048,
        required=True
    )
    hosting_institution_tutor_name = forms.CharField(
        max_length=2048,
        required=True
    )
    hosting_institution_tutor_email = forms.EmailField(
        max_length=2048,
        required=True
    )

    class Meta:
        model = Internship
        exclude = ['created']

    def __init__(self, *args, **kwargs):
        instance = kwargs.get('instance')
        if instance:
            initial = kwargs.get('initial', {})
            initial.update({
                'country': instance.country,
                'company': instance.company,
                'university': instance.university,
                'academic_coordinator': instance.academic_coordinator,
                'academic_tutor': instance.academic_tutor,
                'hosting_institution_tutor': instance.hosting_institution_tutor
            })
            kwargs.update({'initial': initial})
        return super(InternshipAdminForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        if commit:
            internship = super(InternshipAdminForm, self).save(commit=False)

            academic_coordinator = ContactPerson.objects.create(
                name=self.cleaned_data['academic_coordinator_name'], 
                email=self.cleaned_data['academic_coordinator_email']
            )
            academic_tutor = ContactPerson.objects.create(
                name=self.cleaned_data['academic_tutor_name'], 
                email=self.cleaned_data['academic_tutor_email']
            )
            hosting_institution_tutor = ContactPerson.objects.create(
                name=self.cleaned_data['hosting_institution_tutor_name'], 
                email=self.cleaned_data['hosting_institution_tutor_email']
            )
            internship.academic_coordinator = academic_coordinator
            internship.academic_tutor = academic_tutor
            internship.hosting_institution_tutor = hosting_institution_tutor
            internship.save()

            return internship

        return super(InternshipAdminForm, self).save(commit=commit)


class InternshipStudentAdminForm(forms.ModelForm):
    class Meta:
        model = InternshipStudent
        exclude = ['created', 'internship', 'student', 'review', 'university_review', 'company_review']

    def clean(self, *args, **kwargs):
        cleaned_data = super(InternshipStudentAdminForm, self).clean(*args, **kwargs)
        internship = cleaned_data['application'].internship
        if not internship.interns.filter(application=cleaned_data['application'])\
                and internship.interns.count() == internship.seats_number:
            self.add_error('application', _('The maximum number of interns has already been approved'))
        return cleaned_data