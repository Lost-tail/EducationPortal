from datetime import timedelta
import json
from urllib.parse import urlparse

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.core import serializers
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import translation, timezone
from django.utils.translation import gettext as _
from django.utils.timesince import timeuntil

from .forms import (
    AddRepresentativeForm, CompanyForm, ContactPersonForm, InternshipForm, 
    InternshipStudentForm, StudentForm, 
    StudentEducationForm, StudentWorkForm, StudentPublicationForm,
    StudentProfileForm, StudentPhotoForm, StudentMainCVForm, 
    StudentSocialNetworksForm, StudentFilesForm,
    InternshipApplicationForm, InternshipFileForm, RegisterCompanyForm, RegisterStudentForm, 
    RegisterUniversityForm, UniversityForm
)
from .services.services import (
    approve_internship_application, get_activated_companies, get_activated_universities,
    get_companies_for_preview, get_company_by_user, get_internships_for_preview,
    get_object_or_none, get_universities_for_preview, get_university_by_user,
    filter_internship_applications, search_internships, make_user_confirmation_hash_value,
    reject_internship_application, get_university_activated_reviews, get_company_activated_reviews
)
from .services.sending_mail import (
    send_notification_about_new_registered_user, send_signup_confirm_email, 
    send_notification_about_new_application, send_resest_password_confirm_email,
    send_add_representative_confirm_email, send_intern_reviewed_by_organization,
    send_intern_reviewed_by_student, send_notification_university_email
)
from .services.student import (
    edit_current_student_by_form, student_already_applied, get_search_student_skills_json,
    student_applied_to_organization_by_user
)
from .models import (
    Company, Country, Internship, InternshipApplication, InternshipStudent, InternshipReview,
    Language, 
    Student, StudentEducation, StudentWork, StudentPublication, StudentSoftSkill, StudentHardSkill,
    University, UserConfirmation, StaffUser
)
from .utils import convert_int_or_none


def home_view(request):
    context = {
        'countries': Country.objects.all().order_by('name'),
        'internships_for_preview': get_internships_for_preview(),
        'companies_for_preview': get_companies_for_preview(),
        'universities_for_preview': get_universities_for_preview()
    }
    return render(request, 'internships/home.html', context)


def list_internships_view(request):
    university_id = convert_int_or_none(request.GET.get('university_id'))
    country_id = convert_int_or_none(request.GET.get('country_id'))
    company_id = convert_int_or_none(request.GET.get('company_id'))
    num_page = convert_int_or_none(request.GET.get('page', 1))
    keywords = request.GET.get('keywords', '').strip()
    keywords = keywords.split(',') if keywords else None

    page_count_items = 10
    found_internships = search_internships(
        university_id=university_id,
        company_id=company_id,
        country_id=country_id, 
        keywords=keywords
    )
    paginator = Paginator(found_internships, page_count_items)

    context = {
        'countries': Country.objects.all().order_by('name'),
        'pagination_internships': paginator.get_page(num_page),
    }
    return render(request, 'internships/list_internships.html', context)


def internship_detail_view(request, pk):
    context = {
        'internship': get_object_or_404(Internship, pk=pk)
    }
    return render(request, 'internships/internship_detail.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def internship_create_view(request):
    if request.method == 'POST':
        internship_form = InternshipForm(data=request.POST, files=request.FILES)
        academic_coordinator_form = ContactPersonForm({
            'name': request.POST.get('academic_coordinator_name'),
            'email': request.POST.get('academic_coordinator_email'),
        })
        academic_tutor_form = ContactPersonForm({
            'name': request.POST.get('academic_tutor_name'),
            'email': request.POST.get('academic_tutor_email'),
        })
        hosting_institution_tutor_form = ContactPersonForm({
            'name': request.POST.get('hosting_institution_tutor_name'),
            'email': request.POST.get('hosting_institution_tutor_email'),
        })
        if internship_form.is_valid() and academic_coordinator_form.is_valid()\
                and academic_tutor_form.is_valid() and hosting_institution_tutor_form.is_valid():
            internship = internship_form.save(commit=False)
            internship.academic_coordinator = academic_coordinator_form.save()
            internship.academic_tutor = academic_tutor_form.save()
            internship.hosting_institution_tutor = hosting_institution_tutor_form.save()
            internship.university = get_university_by_user(request.user)
            internship.save()
            messages.success(request, _('The internship is saved. The portal administrator will soon check and activate your profile'))
            return redirect(internship.get_detail_url())
    else:
        academic_coordinator_form = academic_tutor_form = hosting_institution_tutor_form = ContactPersonForm()
        internship_form = InternshipForm()

    context = {
        'internship_form': internship_form,
        'academic_coordinator_form': academic_coordinator_form,
        'academic_tutor_form': academic_tutor_form,
        'hosting_institution_tutor_form': hosting_institution_tutor_form,
        'countries': Country.objects.all(),
        'companies': Company.objects.filter(activated=True)
    }
    return render(request, 'internships/internships/create.html', context)


@login_required
@user_passes_test(lambda u: (
    u.is_superuser or hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def internship_edit_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        internship_form = InternshipForm(data=request.POST, files=request.FILES, instance=internship)
        academic_coordinator_form = ContactPersonForm(
            data={
                'name': request.POST.get('academic_coordinator_name'),
                'email': request.POST.get('academic_coordinator_email'),
            },
            instance=internship.academic_coordinator
        )
        academic_tutor_form = ContactPersonForm(
            data={
                'name': request.POST.get('academic_tutor_name'),
                'email': request.POST.get('academic_tutor_email'),
            },
            instance=internship.academic_tutor
        )
        hosting_institution_tutor_form = ContactPersonForm(
            data={
                'name': request.POST.get('hosting_institution_tutor_name'),
                'email': request.POST.get('hosting_institution_tutor_email'),
            },
            instance=internship.hosting_institution_tutor
        )
        if internship_form.is_valid() and academic_coordinator_form.is_valid()\
                and academic_tutor_form.is_valid() and hosting_institution_tutor_form.is_valid():
            internship = internship_form.save(commit=False)
            internship.academic_coordinator = academic_coordinator_form.save()
            internship.academic_tutor = academic_tutor_form.save()
            internship.hosting_institution_tutor = hosting_institution_tutor_form.save()
            internship.save()
            messages.success(request, _('The Internship successful edited'))
    else:
        academic_coordinator_form = ContactPersonForm(instance=internship.academic_coordinator)
        academic_tutor_form = ContactPersonForm(instance=internship.academic_tutor)
        hosting_institution_tutor_form = ContactPersonForm(instance=internship.hosting_institution_tutor)
        internship_form = InternshipForm(instance=internship)
    
    context = {
        'internship': internship,
        'internship_form': internship_form,
        'academic_coordinator_form': academic_coordinator_form,
        'academic_tutor_form': academic_tutor_form,
        'hosting_institution_tutor_form': hosting_institution_tutor_form,
        'countries': Country.objects.all(),
        'companies': Company.objects.filter(activated=True)
    }
    return render(request, 'internships/internships/edit.html', context)



@login_required
@user_passes_test(lambda u: (hasattr(u, 'student') and u.student.confirmed))
def internship_apply_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if not internship.is_applying:
        return redirect('home')

    context = {}
    if request.method == 'POST':
        apply_success = False
        if not student_already_applied(request.user.student, internship):
            data = {
                'cover_letter': request.POST.get('cover_letter'),
                'student': request.user.student,
                'internship': internship
            }
            form = InternshipApplicationForm(data)
            if form.is_valid():
                internship_application = form.save()
                apply_success = True
                send_notification_about_new_application(request, internship_application)

        context['apply_success'] = apply_success

        return render(request, 'internships/internships/apply_result.html', context)

    return render(request, 'internships/internships/apply.html')


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or hasattr(u, 'company') 
    or hasattr(u, 'staff_user')
    and (u.staff_user.staff_type == 'University Representative' 
        or u.staff_type.staff_type == 'Company Representative')
))
def internship_interns_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    num_page = convert_int_or_none(request.GET.get('page', 1))
    context = {
        'internship': internship,
        'pagination_interns': Paginator(internship.interns.all(), per_page=9).get_page(num_page)
    }
    return render(request, 'internships/internships/interns.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def intern_attach_view(request, pk):
    internship_student = get_object_or_404(InternshipStudent, pk=pk)
    if internship_student.student != request.user.student:
        return redirect('student_personal_account')

    if request.method == 'POST':
        form = InternshipStudentForm(data=request.POST, files=request.FILES, instance=internship_student)
        if form.is_valid():
            form.save()
        
    return redirect('student_personal_account')


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'student') or hasattr(u, 'university') or hasattr(u, 'company')
    or hasattr(u, 'staff_user')
    and (u.staff_user.staff_type == 'University Representative' or u.staff_type.staff_type == 'Company Representative')
))
def internship_student_add_review_view(request, pk):
    internship_student = get_object_or_404(InternshipStudent, pk=pk)
    if request.method == 'POST':
        university = get_university_by_user(request.user)
        company = get_company_by_user(request.user)
        if internship_student.internship.university == university:
            text_error = ''
            files = []
            upload_files = request.FILES.getlist('file')
            if len(upload_files) > 5:
                text_error = _('Maximum attachments') + ': 5'
            else:
                for f in request.FILES.getlist('file'):
                    form = InternshipFileForm(files={'file': f})
                    if form.is_valid():
                        files.append(form.save(commit=False))
                    else:
                        text_error = 'File Upload Error'
                        break
            if not text_error:
                review = InternshipReview.objects.create(
                    text=request.POST['text']
                )
                for file in files:
                    file.review = review
                    file.save()
                internship_student.university_review = review
                internship_student.save()
                messages.success(request, _('Reviewed successfully'))
                send_intern_reviewed_by_organization(request, internship_student)
            else:
                messages.error(request, text_error)
            return redirect(internship_student.internship.get_interns_url())
        elif internship_student.internship.company == company:
            text_error = ''
            files = []
            upload_files = request.FILES.getlist('file')
            if len(upload_files) > 5:
                text_error = _('Maximum attachments') + ': 5'
            else:
                for f in request.FILES.getlist('file'):
                    form = InternshipFileForm(files={'file': f})
                    if form.is_valid():
                        files.append(form.save(commit=False))
                    else:
                        print(type(form.errors))
                        text_error = 'File Upload Error'
                        break
            if not text_error:
                review = InternshipReview.objects.create(
                    text=request.POST['text']
                )
                for file in files:
                    file.review = review
                    file.save()
                internship_student.company_review = review
                internship_student.save()
                messages.success(request, _('Reviewed successfully'))
                send_intern_reviewed_by_organization(request, internship_student)
            else:
                messages.error(request, text_error)
            return redirect(internship_student.internship.get_interns_url())
        elif hasattr(request.user, 'student') and internship_student.student == request.user.student:
            text_error = ''
            files = []
            upload_files = request.FILES.getlist('file')
            if len(upload_files) > 5:
                text_error = _('Maximum attachments') + ': 5'
            else:
                for f in request.FILES.getlist('file'):
                    form = InternshipFileForm(files={'file': f})
                    if form.is_valid():
                        files.append(form.save(commit=False))
                    else:
                        text_error = 'File Upload Error'
                        break
            if not text_error:
                review = InternshipReview.objects.create(
                    text=request.POST['text']
                )
                for file in files:
                    file.review = review
                    file.save()
                internship_student.review = review
                internship_student.save()
                messages.success(request, _('Reviewed successfully'))
                send_intern_reviewed_by_student(request, internship_student)
            else:
                messages.error(request, text_error)
            return redirect('student_personal_account')
    return redirect('home')


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def add_university_representative_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({
            'email': data.get('email', '').lower()
        })
        form = AddRepresentativeForm(data)
        if form.is_valid():
            confirmation_user = UserConfirmation.objects.create(
                name=form.cleaned_data['full_name'],
                email=form.cleaned_data['email'],
                password='password',
                user_type='University Representative',
                university=get_university_by_user(request.user)
            )
            confirmation_user.token = make_user_confirmation_hash_value(confirmation_user)
            confirmation_user.save()
            send_add_representative_confirm_email(request, confirmation_user)
            messages.success(request, _('A confirmation email has been sent to the specified email address.'))
    else:
        form = AddRepresentativeForm()
    context = {
        'form': form
    }
    return render(request, 'internships/universities/add_representative.html', context)


def signup_confirm_representative_view(request, pk, token):
    confirmation_user = get_object_or_404(UserConfirmation, pk=pk, token=token)
    if not confirmation_user.user:
        form = AddRepresentativeForm({
            'email': confirmation_user.email, 
            'full_name': confirmation_user.name
        })
        if form.is_valid():
            if request.method == 'POST':
                user = User.objects.create(
                    username=confirmation_user.email,
                    email=confirmation_user.email,
                    password=make_password(request.POST.get('password'))
                )
                confirmation_user.user = user
                confirmation_user.save()
                StaffUser.objects.create(
                    user=user,
                    full_name=confirmation_user.name,
                    staff_type=confirmation_user.user_type,
                    university=confirmation_user.university,
                    company=confirmation_user.company,
                )
                login(request, user)
                return redirect('organization_personal_account')

            return render(request, 'internships/signup_confirm_representative.html')

    return HttpResponseForbidden()


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or hasattr(u, 'company')
    or hasattr(u, 'staff_user')
    and (u.staff_user.staff_type == 'University Representative' or u.staff_type.staff_type == 'Company Representative')
))
def organization_personal_account_view(request):
    num_page = convert_int_or_none(request.GET.get('page', 1))
    user_university = get_university_by_user(request.user)
    user_company = get_company_by_user(request.user)
    if user_university:
        internships = user_university.internships.all()
    elif user_company:
        internships = user_company.internships.all()

    context = {
        'pagination_internships': Paginator(internships, per_page=9).get_page(num_page)
    }
    return render(request, 'internships/organization_personal_account.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or hasattr(u, 'company') 
    or hasattr(u, 'staff_user')
    and (u.staff_user.staff_type == 'University Representative' 
        or u.staff_type.staff_type == 'Company Representative')
))
def internship_applications_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if not (internship.university == get_university_by_user(request.user) 
            or internship.company == get_company_by_user(request.user)):
        return redirect('home')

    num_page = convert_int_or_none(request.GET.get('page', 1))
    applications = filter_internship_applications(
        internship, 
        application_status=request.GET.get('application_status', '')
    )
    context = {
        'pagination_applications': Paginator(applications, per_page=12).get_page(num_page),
        'internship': internship
    }
    return render(request, 'internships/internships/applications.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or hasattr(u, 'company') 
    or hasattr(u, 'staff_user')
    and (u.staff_user.staff_type == 'University Representative' 
        or u.staff_type.staff_type == 'Company Representative')
))
def internship_application_detail_view(request, internship_pk, application_pk):
    application = get_object_or_404(InternshipApplication, pk=application_pk, internship=internship_pk)
    if not (application.internship.university == get_university_by_user(request.user)
            or application.internship.company == get_company_by_user(request.user)):
        return redirect('home')
    context = {'internship_application': application}
    return render(request, 'internships/internships/application_detail.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def internship_application_reject_view(request, internship_pk, application_pk):
    application = get_object_or_404(InternshipApplication, pk=application_pk, internship=internship_pk)
    if not (application.internship.university == get_university_by_user(request.user)):
        return redirect('home')
    reject_internship_application(request, application)
    referer_url = request.META.get('HTTP_REFERER')
    if not referer_url:
        return redirect(application.internship.get_applications_url())
    return HttpResponseRedirect(referer_url)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def internship_application_approve_view(request, internship_pk, application_pk):
    application = get_object_or_404(InternshipApplication, pk=application_pk, internship=internship_pk)
    if not (application.internship.university == get_university_by_user(request.user)):
        return redirect('home')
    approve_internship_application(request, application)
    referer_url = request.META.get('HTTP_REFERER')
    if not referer_url:
        return redirect(application.internship.get_applications_url())
    return HttpResponseRedirect(referer_url)


def list_companies_view(request):
    num_page = convert_int_or_none(request.GET.get('page', 1))

    page_count_items = 10
    paginator = Paginator(get_activated_companies(), page_count_items)

    context = {
        'pagination_companies': paginator.get_page(num_page),
    }
    return render(request, 'internships/list_companies.html', context)


def company_detail_view(request, pk):
    company = get_object_or_404(Company, pk=pk)
    context = {
        'company': company,
        'activated_reviews': get_company_activated_reviews(company)
    }
    return render(request, 'internships/company_detail.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'company') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'Company Representative')
))
def company_edit_view(request):
    company = get_company_by_user(request.user)
    if request.method == 'POST':
        company_form = CompanyForm(data=request.POST, files=request.FILES, instance=company)
        contact_person_form = ContactPersonForm(
            data={
                'name': request.POST.get('contact_person_name'),
                'email': request.POST.get('contact_person_email'),
            }, 
            instance=company.contact_person
        )
        if company_form.is_valid() and contact_person_form.is_valid():
            company = company_form.save(commit=False)
            contact_person = contact_person_form.save()
            company.contact_person = contact_person
            company.save()
            messages.success(request, _('Your profile has been successfully edited'))
            return redirect('organization_personal_account')
    else:
        company_form = CompanyForm(instance=company)

    context = {
        'company': company,
        'form': company_form,
        'countries': Country.objects.all()
    }
    return render(request, 'internships/companies/edit.html', context)


def list_universities_view(request):
    num_page = convert_int_or_none(request.GET.get('page', 1))

    page_count_items = 10
    paginator = Paginator(get_activated_universities(), page_count_items)

    context = {
        'pagination_universities': paginator.get_page(num_page),
    }
    return render(request, 'internships/list_universities.html', context)


def university_detail_view(request, pk):
    university = get_object_or_404(University, pk=pk)
    context = {
        'university': university,
        'activated_reviews': get_university_activated_reviews(university)
    }
    return render(request, 'internships/university_detail.html', context)



@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def university_edit_view(request):
    university = get_university_by_user(request.user)
    if request.method == 'POST':
        university_form = UniversityForm(data=request.POST, files=request.FILES, instance=university)
        contact_person_form = ContactPersonForm(
            data={
                'name': request.POST.get('contact_person_name'),
                'email': request.POST.get('contact_person_email'),
            }, 
            instance=university.contact_person
        )
        if university_form.is_valid() and contact_person_form.is_valid():
            university = university_form.save(commit=False)
            contact_person = contact_person_form.save()
            university.contact_person = contact_person
            university.save()
            messages.success(request, _('Your profile has been successfully edited'))
            return redirect('organization_personal_account')
    else:
        university_form = UniversityForm(instance=university)

    context = {
        'university': university,
        'form': university_form,
        'countries': Country.objects.all()
    }
    return render(request, 'internships/universities/edit.html', context)


@login_required
@user_passes_test(lambda u: (
    hasattr(u, 'university') or (hasattr(u, 'staff_user') 
        and u.staff_user.staff_type == 'University Representative')
))
def university_students_view(request):
    university = get_university_by_user(request.user)
    if request.method == 'POST':
        confirm = request.POST.get('confirm')
        if confirm:
            obj = Student.objects.filter(id=confirm)[0]
            obj.confirmed = True
            obj.save()
        else:
            data = request.POST.dict()
            obj = Student.objects.filter(id=request.POST.get('user_id'))[0]
            obj.academic_merit = data['academic_merit']
            obj.research_experience = data['research_experience']
            obj.motivation = data['motivation']
            obj.language_skill = data['language_skill']
            obj.overall = (int(data['academic_merit']) + int(data['research_experience']) + int(data['motivation'])+ int(data['language_skill']))//4
            obj.save()
    students = Student.objects.filter(university=university).order_by('confirmed')
    num_page = convert_int_or_none(request.GET.get('page', 1))
    context = {
        'pagination_students': Paginator(students, per_page=9).get_page(num_page)
    }
    return render(request, 'internships/university_students.html', context)

@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_personal_account_view(request):
    num_page = convert_int_or_none(request.GET.get('page', 1))
    paginator = Paginator(request.user.student.internships_applications.all(), per_page=12)
    context = {
        'pagination_internships_applications': paginator.get_page(num_page),
    }
    return render(request, 'internships/students/personal_account.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_internship_application_detail(request, pk):
    internship_application = get_object_or_404(
        InternshipApplication, pk=pk, student=request.user.student
    )
    context = {
        'internship_application': internship_application
    }
    return render(request, 'internships/students/application_internship_detail.html', context)


@login_required
def student_detail_view(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if not ((hasattr(request.user, 'student') and request.user.student == student) 
            or request.user.is_superuser or student_applied_to_organization_by_user(student, request.user)):
        return redirect('home')

    context = {
        'student': student,
    }
    return render(request, 'internships/student_detail.html', context)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_edit_view(request):
    form, updated = edit_current_student_by_form(request=request, form_class=StudentForm)
    print(form.errors)
    if updated:
        messages.success(request, _('Your profile has been successfully edited'))
        return redirect('student_edit')


    context = {
        'form': form,
        'education_form': StudentEducationForm(),
        'countries': Country.objects.all(),
        'languages': Language.objects.all(),
        'universities': get_activated_universities()
    }
    return render(request, 'internships/students/edit.html', context)



@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_publication_create_view(request):
    if request.method == 'POST':
        form = StudentPublicationForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user.student
            obj.save()
    return redirect('student_edit')


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_publication_edit_view(request, pk):
    student_publication = get_object_or_404(StudentPublication, pk=pk)
    if student_publication.student != request.user.student:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StudentPublicationForm(data=request.POST, instance=student_publication)
        if form.is_valid():
            form.save()

    return redirect('student_edit')


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def student_publication_delete_view(request, pk):
    student_publication = get_object_or_404(StudentPublication, pk=pk)
    if student_publication.student != request.user.student:
        return HttpResponseForbidden()

    student_publication.delete()

    return redirect('student_edit')


def search_student_skills_view(request):
    search_name = request.GET.get('name', '')
    skill_type = request.GET.get('skill_type', '')
    response_data = {
        'student_skills': get_search_student_skills_json(name=search_name, skill_type=skill_type)
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_educuation_create_view(request):
    response_data = {}
    if request.method == 'POST':
        form = StudentEducationForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user.student
            obj.save()

    response_data = {
        'student_education': json.loads(serializers.serialize(
            'json', 
            StudentEducation.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_education_edit_view(request, pk):
    student_education = get_object_or_404(StudentEducation, pk=pk)
    if student_education.student != request.user.student:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StudentEducationForm(data=request.POST, instance=student_education)
        if form.is_valid():
            form.save()

    response_data = {
        'student_education': json.loads(serializers.serialize(
            'json', 
            StudentEducation.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def api_student_education_delete_view(request, pk):
    student_education = get_object_or_404(StudentEducation, pk=pk)
    if student_education.student != request.user.student:
        return HttpResponseForbidden()

    student_education.delete()
    response_data = {
        'student_education': json.loads(serializers.serialize(
            'json', 
            StudentEducation.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_work_create_view(request):
    response_data = {}
    if request.method == 'POST':
        form = StudentWorkForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user.student
            obj.save()

    response_data = {
        'student_work': json.loads(serializers.serialize(
            'json', 
            StudentWork.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_work_edit_view(request, pk):
    student_work = get_object_or_404(StudentWork, pk=pk)
    if student_work.student != request.user.student:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StudentWorkForm(data=request.POST, instance=student_work)
        if form.is_valid():
            form.save()

    response_data = {
        'student_work': json.loads(serializers.serialize(
            'json', 
            StudentWork.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
def api_student_work_delete_view(request, pk):
    student_work = get_object_or_404(StudentWork, pk=pk)
    if student_work.student != request.user.student:
        return HttpResponseForbidden()

    student_work.delete()

    response_data = {
        'student_work': json.loads(serializers.serialize(
            'json', 
            StudentWork.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_publication_create_view(request):
    response_data = {}
    if request.method == 'POST':
        form = StudentPublicationForm(data=request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.student = request.user.student
            obj.save()

    response_data = {
        'student_publication': json.loads(serializers.serialize(
            'json', 
            StudentPublication.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_publication_edit_view(request, pk):
    student_publication = get_object_or_404(StudentPublication, pk=pk)
    if student_publication.student != request.user.student:
        return HttpResponseForbidden()

    if request.method == 'POST':
        form = StudentPublicationForm(data=request.POST, instance=student_publication)
        if form.is_valid():
            form.save()

    response_data = {
        'student_publication': json.loads(serializers.serialize(
            'json', 
            StudentPublication.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_publication_delete_view(request, pk):
    student_publication = get_object_or_404(StudentPublication, pk=pk)
    if student_publication.student != request.user.student:
        return HttpResponseForbidden()

    student_publication.delete()

    response_data = {
        'student_publication': json.loads(serializers.serialize(
            'json', 
            StudentPublication.objects.filter(student=request.user.student)
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_skill_add_view(request):
    skill_class = StudentSoftSkill
    if request.method == 'POST':
        skill_name = request.POST.get('name', '').lower().strip()
        skill_type = request.POST.get('skill_type')
        if skill_type == 'soft':
            skill_class = StudentSoftSkill
        elif skill_type == 'hard':
            skill_class = StudentHardSkill
        else:
            return HttpResponseForbidden()

        if skill_name:
            skill, _ = skill_class.objects.get_or_create(name=skill_name)
            skill.students.add(request.user.student)

    if skill_class == StudentSoftSkill:
        skills = request.user.student.soft_skills.all()
    elif skill_class == StudentHardSkill:
        skills = request.user.student.hard_skills.all()

    response_data = {
        'student_skills': json.loads(serializers.serialize(
            'json', 
            skills
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_skill_remove_view(request, pk):
    skill_type = request.GET.get('skill_type')
    if skill_type == 'soft':
        skill_class = StudentSoftSkill
    elif skill_type == 'hard':
        skill_class = StudentHardSkill
    else:
        raise HttpResponseForbidden()

    skill = get_object_or_404(skill_class, pk=pk)
    if skill_class == StudentSoftSkill:
        request.user.student.soft_skills.remove(skill)
        skills = request.user.student.soft_skills.all()
    elif skill_class == StudentHardSkill:
        request.user.student.hard_skills.remove(skill)
        skills = request.user.student.hard_skills.all()

    response_data = {
        'student_skills': json.loads(serializers.serialize(
            'json', 
            skills
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_language_add_view(request):
    if request.method == 'POST':
        language = get_object_or_none(Language, pk=request.POST.get('pk', 0))
        if language:
            request.user.student.languages.add(language)

    response_data = {
        'student_languages': json.loads(serializers.serialize(
            'json', 
            request.user.student.languages.all()
        ))
    }
    return JsonResponse(response_data)


@login_required
@user_passes_test(lambda u: hasattr(u, 'student'))
@csrf_exempt
def api_student_language_remove_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    request.user.student.languages.remove(language)

    response_data = {
        'student_languages': json.loads(serializers.serialize(
            'json', 
            request.user.student.languages.all()
        ))
    }
    return JsonResponse(response_data)

    

def about_us_view(request):
    return render(request, 'internships/about_us.html')


def contact_us_view(request):
    return render(request, 'internships/contact_us.html')



def signup_view(request):
    form = None
    context = {}
    if request.method == 'POST':
        signup_type = request.POST.get('signup_type')
        data = request.POST.dict()
        data['email'] = data.get('email', '').lower().strip()
        if signup_type == 'student':
            form = RegisterStudentForm(data)
        elif signup_type == 'company':
            form = RegisterCompanyForm(data)
        elif signup_type == 'university':
            form = RegisterUniversityForm(data)
        if form and form.is_valid():
            name = form.cleaned_data['full_name'] if signup_type == 'student'\
                else form.cleaned_data['name']
            confirmation_user = UserConfirmation(
                name=name,
                email=form.cleaned_data['email'],
                password=make_password(form.cleaned_data['password']),
                user_type=signup_type,
                card_number=form.cleaned_data['card_number'],
                university=form.cleaned_data['university']
            )
            confirmation_user.token = make_user_confirmation_hash_value(confirmation_user)
            confirmation_user.save()
            send_signup_confirm_email(request, confirmation_user)
            messages.success(
                request, 
                _('A confirmation email has been sent to your email') + f' "{confirmation_user.email}"'
            )
            
            return render(request, 'internships/signup.html')

        context['signup_type'] = signup_type

    context['form'] = form
    context['universities'] = University.objects.all()

    return render(request, 'internships/signup.html', context)


def signup_confirm_email_view(request, pk, token):
    confirmation_user = get_object_or_404(UserConfirmation, pk=pk, token=token)
    if not confirmation_user.user:
        form = None
        data = {
            'name': confirmation_user.name,
            'email': confirmation_user.email.lower(), 
            'password': confirmation_user.password,
            'university': confirmation_user.university,
            'card_number': confirmation_user.card_number
        }
        if confirmation_user.user_type == 'student':
            del data['name']
            data['full_name'] = confirmation_user.name
            form = RegisterStudentForm(data)
        elif confirmation_user.user_type == 'company':
            form = RegisterCompanyForm(data)
        elif confirmation_user.user_type == 'university':
            form = RegisterUniversityForm(data)

        if form and form.is_valid():
            obj = form.save(commit=False)
            user = User.objects.create(
                username=form.cleaned_data['email'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            confirmation_user.user = user
            obj.user = user
            obj.university = form.cleaned_data['university']
            obj.card_number = form.cleaned_data['card_number']
            confirmation_user.save()
            obj.save()
            send_notification_about_new_registered_user(request, confirmation_user)
            send_notification_university_email(obj)
            login(request, user)
            return redirect('home')

    return HttpResponseForbidden()
    

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        if email and password:
            user = get_object_or_none(User, email=email)
            if user and user.check_password(password):
                login(request, user)
                if get_university_by_user(user) or get_company_by_user(user):
                    redirect_url_name = 'organization_personal_account'
                elif hasattr(user, 'student'):
                    redirect_url_name = 'student_personal_account'
                else:
                    redirect_url_name = 'home'
                return redirect(request.GET.get('next', redirect_url_name))
        messages.error(request, _('Incorrect email or password'))
    return render(request, 'internships/login.html')


def logout_view(request):
    logout(request)
    return redirect('home')


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        user = get_object_or_none(User, email=email)
        if user:
            if not hasattr(user, 'confirmation'):
                if hasattr(user, 'student'):
                    user_type = 'student'
                elif hasattr(user, 'staff_user'):
                    user_type = user.staff_user.staff_type
                elif hasattr(user, 'university'):
                    user_type = 'university'
                elif hasattr(user, 'company'):
                    user_type = 'company'
                else:
                    return redirect('home')

                confirmation_user = UserConfirmation.objects.create(
                    name='UserName',
                    email=user.email,
                    password=user.password,
                    user_type=user_type,
                    user=user
                )
                user.confirmation = confirmation_user
                user.save()
            else:
                confirmation_user = user.confirmation
            confirmation_user.token = make_user_confirmation_hash_value(confirmation_user)
            confirmation_user.reseted = False
            confirmation_user.save()
            send_resest_password_confirm_email(request, confirmation_user)


        messages.success(request, _('Check your email for a link to reset your password.'))
    return render(request, 'internships/forgot_password.html')


def reset_password_view(request, pk, token):
    confirmation_user = get_object_or_404(UserConfirmation, pk=pk, token=token)
    if timezone.now() - confirmation_user.updated < timedelta(days=1)\
            and not confirmation_user.reseted:
        if request.method == 'POST':
            new_password = request.POST.get('password')
            confirmation_user.user.set_password(new_password)
            confirmation_user.user.save()
            confirmation_user.reseted = True
            confirmation_user.save()
            return redirect('login')
        context = {'confirmation_user': confirmation_user}
        return render(request, 'internships/reset_password.html', context)
    return HttpResponseForbidden()


def set_lang_view(request):
    language = request.GET.get('lang', settings.LANGUAGE_CODE)
    next_url = request.GET.get('next', '/')
    translation.activate(language)
    response = HttpResponseRedirect(next_url)
    response.set_cookie(settings.LANGUAGE_COOKIE_NAME, language)
    return response


def handler404(request, *args, **argv):
    return render(request, 'internships/404.html')


def handler_server_error(request, *args, **argv):
    response = render(request, 'internships/server_error.html')
    return response
