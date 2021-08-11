import six

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Q
from django.utils import timezone
from django.utils.translation import gettext as _

from internships.models import Company, Internship, InternshipStudent, InternshipApplication, University
from .sending_mail import (
    send_notification_approved_internship_application, send_notification_rejected_internship_application
)


def search_internships(country_id=None, keywords=None, company_id=None, university_id=None):
    internships = Internship.objects.filter(activated=True, university__activated=True, company__activated=True)
    if company_id:
        internships = internships.filter(company__id=company_id)
    if university_id:
        internships = internships.filter(university__id=university_id)
    if country_id:
        internships = internships.filter(country__id=country_id)
    if keywords:
        query = Q()
        for keyword in keywords:
            query |= (
                Q(name__icontains=keyword)
                | Q(description__icontains=keyword)
                | Q(required_knowledge__icontains=keyword)
                | Q(objectives__icontains=keyword)
                | Q(short_course_modules__icontains=keyword)
                | Q(additional_notes__icontains=keyword)
                | Q(company__name__icontains=keyword)
                | Q(university__name__icontains=keyword)
            )
        internships = internships.filter(query)
    return internships


def get_internships_for_preview():
    return Internship.objects.filter(
        activated=True, university__activated=True, company__activated=True
    )[:4]


def get_companies_for_preview():
    return get_activated_companies()[:6]


def get_universities_for_preview():
    return get_activated_universities()[:6]


def get_activated_companies():
    return Company.objects.filter(activated=True)


def get_activated_universities():
    return University.objects.filter(activated=True)


def get_object_or_none(obj_class, **fields):
    try:
        return obj_class.objects.get(**fields)
    except obj_class.DoesNotExist:
        return None


def user_email_already_exist(email):
    if get_object_or_none(User, email=email) or get_object_or_none(User, username=email):
        return True
    return False


def make_user_confirmation_hash_value(user_confirmation):
    timestamp = timezone.now().timestamp()
    return (
        six.text_type(user_confirmation.pk) + user_confirmation.password + six.text_type(timestamp)
    ).replace('/', '')


def get_university_by_user(user):
    if hasattr(user, 'university'):
        return user.university
    elif hasattr(user, 'staff_user') and user.staff_user.staff_type == 'University Representative':
        return user.staff_user.university
    return None


def get_company_by_user(user):
    if hasattr(user, 'company'):
        return user.company
    elif hasattr(user, 'staff_user') and user.staff_user.staff_type == 'Company Representative':
        return user.staff_user.company
    return None


def filter_internship_applications(internship, application_status=''):
    applications = internship.applications.all()
    if application_status:
        applications = applications.filter(status=application_status)
    return applications


def approve_internship_application(request, application):
    internship = application.internship
    if internship.interns.count() < internship.seats_number:
        InternshipStudent.objects.create(
            internship=internship,
            student=application.student,
            application=application
        )
        application.status = InternshipApplication.Statuses.APPROVED
        application.save()
        messages.success(request, _('Application has been successfully approved'))
        send_notification_approved_internship_application(request, application)
    else:
        messages.error(request, _('The maximum number of interns has already been approved'))


def reject_internship_application(request, internship_application):
    internship_application.status = InternshipApplication.Statuses.REJECTED
    internship_application.save()
    send_notification_rejected_internship_application(request, internship_application)


def check_internships():
    now_date = timezone.now().date()
    Internship.objects.filter(status='CALL', applications_deadline__lte=now_date).update(
        status='ENROLL'
    )
    Internship.objects.filter(status='ENROLL', start_date__lte=now_date).update(
        status='INTERNSHIP'
    )
    Internship.objects.filter(status='INTERNSHIP', end_date__lte=now_date).update(
        status='CLOSE'
    )


def get_university_activated_reviews(university):
    reviews = []
    for internship in university.internships.filter(status='CLOSE'):
        for internship_student in internship.interns.all():
            if internship_student.review and internship_student.review.activated:
                reviews.append(internship_student.review)
    return reviews


def get_company_activated_reviews(company):
    reviews = []
    for internship in company.internships.filter(status='CLOSE'):
        for internship_student in internship.interns.all():
            if internship_student.review and internship_student.review.activated:
                reviews.append(internship_student.review)
    return reviews