from django.contrib import messages
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from internships.forms import (
    ContactPersonForm, CountryForm, InternshipForm, InternshipApplicationForm,
    LanguageForm, StaffUserForm, RegisterStaffUserForm,
    RegisterUniversityForm, RegisterCompanyForm, RegisterStudentForm, UniversityForm,
    InternshipFileForm
)
from internships.services.services import get_object_or_none
from internships.models import (
    Company, Country, Internship, InternshipApplication, InternshipStudent, 
    Language, Student, StaffUser, University, InternshipReview
)
from internships.utils import convert_int_or_none
from .forms import (
    CompanyAdminForm, InternshipAdminForm, 
    InternshipStudentAdminForm, StudentAdminForm, UniversityAdminForm
)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internships_list_view(request):
    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_internships = Internship.objects.all()
    paginator = Paginator(all_internships, page_count_items)

    context = {
        'pagination_internships': paginator.get_page(num_page),
    }
    return render(request, 'admins/internships_list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_create_view(request):
    if request.method == 'POST':
        form = InternshipAdminForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            return redirect('internships_list')
    else:
        form = InternshipAdminForm(data=request.GET)
    context = {
        'internship_form': form,
        'countries': Country.objects.all(),
        'сompanies': Company.objects.all(),
        'universities': University.objects.all()
    }
    return render(request, 'admins/internship_create.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_edit_view(request, pk):
    internship = get_object_or_404(Internship, pk=pk)
    if request.method == 'POST':
        form = InternshipAdminForm(data=request.POST, files=request.FILES, instance=internship)
        if form.is_valid():
            internship = form.save()
            messages.success(request, 'Internship Successfully Saved')
            return redirect(internship.get_edit_url())
    else:   
        form = InternshipAdminForm(instance=internship)

    context = {
        'internship_form': form,
        'countries': Country.objects.all(),
        'сompanies': Company.objects.all(),
        'universities': University.objects.all()
    }
    return render(request, 'admins/internship_edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_delete_view(request, pk):
    obj = get_object_or_404(Internship, pk=pk)
    obj.delete()
    messages.success(request, 'Internship Successfully Deleted')
    return redirect('internships_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_applications_list_view(request, internship_pk):
    internship = get_object_or_404(Internship, pk=internship_pk)
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'internship': internship})
        form = InternshipApplicationForm(
            data=data, 
            files=request.FILES
        )
        if form.is_valid():
            internship_application = form.save()
            messages.success(request, 'Internship Application Successfully Saved')
            return redirect(internship_application.get_admin_edit_url())
    else:   
        form = InternshipApplicationForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    paginator = Paginator(internship.applications.all(), per_page=20)
    context = {
        'form': form,
        'internship': internship,
        'pagination_applications': paginator.get_page(num_page),
        'students': Student.objects.all()
    }
    return render(request, 'admins/internships/applications/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_applications_edit_view(request, pk):
    internship_application = get_object_or_404(InternshipApplication, pk=pk)
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({'internship': internship_application.internship})
        form = InternshipApplicationForm(
            data=data, 
            files=request.FILES,
            instance=internship_application
        )
        if form.is_valid():
            internship_application = form.save()
            messages.success(request, 'Internship Application Successfully Saved')
            return redirect(internship_application.get_admin_edit_url())
    else:   
        form = InternshipApplicationForm(instance=internship_application)

    context = {
        'form': form,
        'internship_application': internship_application,
        'students': Student.objects.all()
    }
    return render(request, 'admins/internships/applications/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_application_delete_view(request, pk):
    obj = get_object_or_404(InternshipApplication, pk=pk)
    internship = obj.internship
    obj.delete()
    messages.success(request, 'Intern Successfully Deleted')
    return redirect(internship.get_admin_applications_url())


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_interns_list_view(request, internship_pk):
    internship = get_object_or_404(Internship, pk=internship_pk)
    if request.method == 'POST':
        internship = get_object_or_404(Internship, pk=internship_pk)
        form = InternshipStudentAdminForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            internship_student = form.save(commit=False)
            internship_student.internship = internship
            internship_student.student = internship_student.application.student
            internship_student.save()
            messages.success(request, 'Intern Successfully Saved')
            return redirect(internship_student.get_admin_edit_url())
    else:   
        form = InternshipStudentAdminForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    paginator = Paginator(internship.interns.all(), per_page=20)
    context = {
        'internship': internship,
        'pagination_interns': paginator.get_page(num_page),
        'form': form,
        'applications': internship.applications.filter(status='APPROVED')
    }
    return render(request, 'admins/internships/interns/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_student_edit_view(request, pk):
    internship_student = get_object_or_404(InternshipStudent, pk=pk)
    if request.method == 'POST':
        form = InternshipStudentAdminForm(data=request.POST, files=request.FILES, instance=internship_student)
        if form.is_valid():
            internship_student = form.save()
            student_review_activated = request.POST.get('student_review_activated')
            student_review_text = request.POST.get('student_review')
            university_review_text = request.POST.get('university_review')
            company_review_text = request.POST.get('company_review')
            if student_review_text:
                if student_review_activated:
                    activated = True
                else:
                    activated = False
                if internship_student.review:
                    internship_student.review.text = student_review_text
                    internship_student.review.activated = activated
                    internship_student.review.save()
                else:
                    internship_student.review = InternshipReview.objects.create(
                        activated=activated,
                        text=student_review_text
                    )
                    internship_student.save()
            if university_review_text:
                if internship_student.university_review:
                    internship_student.university_review.text = university_review_text
                    internship_student.university_review.save()
                else:
                    internship_student.university_review = InternshipReview.objects.create(
                        text=university_review_text
                    )
                    internship_student.save()
            if company_review_text:
                if internship_student.company_review:
                    internship_student.company_review.text = company_review_text
                    internship_student.company_review.save()
                else:
                    internship_student.company_review = InternshipReview.objects.create(
                        text=company_review_text
                    )
                    internship_student.save()
            messages.success(request, 'Intern Successfully Saved')
            return redirect(internship_student.get_admin_edit_url())
    else:   
        form = InternshipStudentAdminForm(instance=internship_student)

    context = {
        'form': form,
        'internship_student': internship_student,
        'applications': internship_student.internship.applications.filter(
            status='APPROVED', student=internship_student.student
        ),
    }
    return render(request, 'admins/internships/interns/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def internship_student_delete_view(request, pk):
    obj = get_object_or_404(InternshipStudent, pk=pk)
    internship = obj.internship
    obj.delete()
    messages.success(request, 'Intern Successfully Deleted')
    return redirect(internship.get_admin_interns_url())


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def universities_list_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data['email'] = data.get('email', '').strip().lower()
        short_university_form = RegisterUniversityForm(data)
        if short_university_form.is_valid():
            university = short_university_form.save(commit=False)
            user = User(
                email=short_university_form.cleaned_data['email'],
                username=short_university_form.cleaned_data['email'],
            )
            user.set_password(short_university_form.cleaned_data['password'])
            user.save()
            university.user = user
            university.save()
            messages.success(request, 'University Successfully Сreated')
            return redirect(university.get_admin_edit_url())
    else:
        short_university_form = RegisterUniversityForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_universities = University.objects.all()
    paginator = Paginator(all_universities, page_count_items)

    context = {
        'pagination_universities': paginator.get_page(num_page),
        'short_university_form': short_university_form
    }
    return render(request, 'admins/universities/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def university_edit_view(request, pk):
    university = get_object_or_404(University, pk=pk)
    if request.method == 'POST':
        university_form = UniversityAdminForm(
            data=request.POST, 
            files=request.FILES, 
            instance=university
        )
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

            messages.success(request, 'University Successfully Saved')
            return redirect(university.get_admin_edit_url())
    else:   
        university_form = UniversityAdminForm(instance=university)
    context = {
        'university_form': university_form,
        'countries': Country.objects.all()
    }
    return render(request, 'admins/universities/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def university_delete_view(request, pk):
    obj = get_object_or_404(University, pk=pk)
    obj.user.delete()
    messages.success(request, 'University Successfully Deleted')
    return redirect('universities_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def companies_list_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data['email'] = data.get('email', '').strip().lower()
        register_company_form = RegisterCompanyForm(data)
        if register_company_form.is_valid():
            company = register_company_form.save(commit=False)
            user = User(
                email=register_company_form.cleaned_data['email'],
                username=register_company_form.cleaned_data['email'],
            )
            user.set_password(register_company_form.cleaned_data['password'])
            user.save()
            company.user = user
            company.save()
            messages.success(request, 'Company Successfully Сreated')
            return redirect(company.get_admin_edit_url())
    else:
        register_company_form = RegisterCompanyForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_companies = Company.objects.all()
    paginator = Paginator(all_companies, page_count_items)

    context = {
        'pagination_companies': paginator.get_page(num_page),
        'register_company_form': register_company_form
    }
    return render(request, 'admins/companies/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def company_edit_view(request, pk):
    company = get_object_or_none(Company, pk=pk)
    if request.method == 'POST':
        company_form = CompanyAdminForm(
            data=request.POST, 
            files=request.FILES, 
            instance=company
        )
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

            messages.success(request, 'Company Successfully Saved')
            return redirect(company.get_admin_edit_url())
    else:   
        company_form = CompanyAdminForm(instance=company)

    context = {
        'company_form': company_form,
        'countries': Country.objects.all()
    }
    return render(request, 'admins/companies/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def company_delete_view(request, pk):
    obj = get_object_or_404(Company, pk=pk)
    obj.user.delete()
    messages.success(request, 'Company Successfully Deleted')
    return redirect('companies_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def staff_users_list_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data['email'] = data.get('email', '').strip().lower()
        staff_user_form = RegisterStaffUserForm(data)
        if staff_user_form.is_valid():
            staff_user = staff_user_form.save(commit=False)
            user = User(
                email=staff_user_form.cleaned_data['email'],
                username=staff_user_form.cleaned_data['email'],
            )
            user.set_password(staff_user_form.cleaned_data['password'])
            if staff_user.staff_type == 'SuperAdmin':
                user.is_staff = True
                user.is_superuser = True
            user.save()
            staff_user.user = user
            staff_user.save()
            messages.success(request, 'Staff User Successfully Сreated')
            return redirect(staff_user.get_admin_edit_url())
    else:
        staff_user_form = RegisterStaffUserForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_staff_users = StaffUser.objects.all()
    paginator = Paginator(all_staff_users, page_count_items)

    context = {
        'staff_user_form': staff_user_form,
        'pagination_staff_users': paginator.get_page(num_page),
        'universities': University.objects.all(),
        'companies': Company.objects.all()
    }
    return render(request, 'admins/staff_users/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def staff_user_edit_view(request, pk):
    staff_user = get_object_or_404(StaffUser, pk=pk)
    if request.method == 'POST':
        form = StaffUserForm(data=request.POST, instance=staff_user)
        if form.is_valid():
            staff_user = form.save(commit=False)
            staff_user.user.email = form.cleaned_data['email']
            staff_user.user.username = form.cleaned_data['email']
            staff_user.user.save()
            staff_user.save()
            messages.success(request, 'Staff User Successfully Saved')
            return redirect(staff_user.get_admin_edit_url())
    else:   
        form = StaffUserForm(instance=staff_user)

    context = {
        'staff_user_form': form,
        'staff_user': staff_user,
        'universities': University.objects.all(),
        'companies': Company.objects.all()
    }
    return render(request, 'admins/staff_users/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def staff_user_delete_view(request, pk):
    staff_user = get_object_or_404(StaffUser, pk=pk)
    staff_user.user.delete()
    messages.success(request, 'Staff User Successfully Deleted')
    return redirect('staff_users_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def countries_list_view(request):
    if request.method == 'POST':
        country_form = CountryForm(request.POST)
        if country_form.is_valid():
            country_form.save()
            messages.success(request, 'Сountry Successfully Сreated')
    else:
        country_form = CountryForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_countries = Country.objects.all()
    paginator = Paginator(all_countries, page_count_items)

    context = {
        'country_form': country_form,
        'pagination_countries': paginator.get_page(num_page)
    }
    return render(request, 'admins/countries/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def country_edit_view(request, pk):
    country = get_object_or_404(Country, pk=pk)
    if request.method == 'POST':
        country_form = CountryForm(request.POST, instance=country)
        if country_form.is_valid():
            country_form.save()
            messages.success(request, 'Country Successfully Saved')
            return redirect('countries_list')
    else:
        country_form = CountryForm(instance=country)
        
    context = {
        'country_form': country_form,
    }
    return render(request, 'admins/countries/edit.html', context)



@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def country_delete_view(request, pk):
    obj = get_object_or_404(Country, pk=pk)
    obj.delete()
    messages.success(request, 'Country Successfully Deleted')
    return redirect('countries_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def languages_list_view(request):
    if request.method == 'POST':
        language_form = LanguageForm(request.POST)
        if language_form.is_valid():
            language_form.save()
            messages.success(request, 'Language Successfully Сreated')
    else:
        language_form = LanguageForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    page_count_items = 20

    all_languages = Language.objects.all()
    paginator = Paginator(all_languages, page_count_items)

    context = {
        'language_form': language_form,
        'pagination_languages': paginator.get_page(num_page)
    }
    return render(request, 'admins/languages/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def language_edit_view(request, pk):
    language = get_object_or_404(Language, pk=pk)
    if request.method == 'POST':
        language_form = LanguageForm(request.POST, instance=language)
        if language_form.is_valid():
            language_form.save()
            messages.success(request, 'Language Successfully Saved')
            return redirect('languages_list')
    else:
        language_form = LanguageForm(instance=language)

    context = {
        'language_form': language_form,
    }
    return render(request, 'admins/languages/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def language_delete_view(request, pk):
    obj = get_object_or_404(Language, pk=pk)
    obj.delete()
    messages.success(request, 'Language Successfully Deleted')
    return redirect('languages_list')


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def students_list_view(request):
    if request.method == 'POST':
        data = request.POST.dict()
        data['email'] = data.get('email', '').strip().lower()
        register_student_form = RegisterStudentForm(data)
        if register_student_form.is_valid():
            student = register_student_form.save(commit=False)
            user = User(
                email=register_student_form.cleaned_data['email'],
                username=register_student_form.cleaned_data['email'],
            )
            user.set_password(register_student_form.cleaned_data['password'])
            user.save()
            student.user = user
            student.save()
            messages.success(request, 'Student Successfully Сreated')
            return redirect(student.get_admin_edit_url())
    else:
        register_student_form = RegisterCompanyForm()

    num_page = convert_int_or_none(request.GET.get('page', 1))
    paginator = Paginator(Student.objects.all(), per_page=20)

    context = {
        'pagination_students': paginator.get_page(num_page),
        'register_student_form': register_student_form
    }
    return render(request, 'admins/students/list.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def student_edit_view(request, pk):
    student = get_object_or_none(Student, pk=pk)
    if request.method == 'POST':
        data = request.POST.dict()
        data.update({
            'birthdate': '/'.join(data['birthdate'].split('-')[::-1])
        })
        form = StudentAdminForm(
            data=data, 
            files=request.FILES, 
            instance=student
        )
        if form.is_valid():
            student = form.save()
            messages.success(request, 'Student Successfully Saved')
            return redirect(student.get_admin_edit_url())
    else:   
        form = StudentAdminForm(instance=student)

    context = {
        'form': form,
        'countries': Country.objects.all(),
        'student': student
    }
    return render(request, 'admins/students/edit.html', context)


@login_required
@user_passes_test(test_func=lambda u: u.is_superuser)
def student_delete_view(request, pk):
    obj = get_object_or_404(Student, pk=pk)
    obj.user.delete()
    messages.success(request, 'Student Successfully Deleted')
    return redirect('students_list')


def login_view(request):
    if request.user.is_authenticated and request.user.is_superuser:
        return redirect('internships_list')

    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password')
        if email and password:
            user = get_object_or_none(User, email=email)
            if user and user.check_password(password) and user.is_superuser:
                login(request, user)
                return redirect(request.GET.get('next', 'internships_list'))
    return render(request, 'admins/login.html')


def logout_view(request):
    logout(request)
    return redirect('login')