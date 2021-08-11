import threading

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string


MAIN_DOMAIN = 'https://work4practice.com'
ADMIN_DOMAIN = 'https://admin.work4practice.com'


class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)

    def run(self):
        self.email.send(fail_silently=False)


def send_signup_confirm_email(request, confirmation_user):
    context = {
        'confirmation_user': confirmation_user, 
        'domain': get_current_site(request)
    }
    subject = 'HEIs Employers / Confirm Email'
    message = render_to_string('internships/emails/register_confirm_email.html', context)
    email = EmailMessage(subject, message, to=[confirmation_user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_notification_university_email(user):
    context = {
        'student': user
    }
    subject = 'HEIs Employers / Notification Email'
    message = render_to_string('internships/emails/notification_university_email.html', context)
    email = EmailMessage(subject, message, to=[user.university.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_notification_approved_internship_application(request, internship_application):
    context = {
        'internship_application': internship_application,
        'domain': get_current_site(request)
    }
    subject = f'HEIs Employers / {internship_application.internship.name} / Approved'
    message = render_to_string('internships/emails/approved_internship_application_student.html', context)
    email = EmailMessage(subject, message, to=[internship_application.student.user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_notification_rejected_internship_application(request, internship_application):
    context = {
        'internship_application': internship_application,
        'domain': get_current_site(request)
    }
    subject = f'HEIs Employers / {internship_application.internship.name} / Rejected'
    message = render_to_string('internships/emails/rejected_internship_application_student.html', context)
    email = EmailMessage(subject, message, to=[internship_application.student.user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_notification_about_new_application(request, internship_application):
    context = {
        'internship_application': internship_application,
        'domain': get_current_site(request)
    }
    subject = f'HEIs Employers / {internship_application.internship.name} / New Application'
    message = render_to_string('internships/emails/created_application_for_student.html', context)
    email = EmailMessage(subject, message, to=[internship_application.student.user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()

    message = render_to_string('internships/emails/created_application_for_university.html', context)
    email = EmailMessage(subject, message, to=[internship_application.internship.university.user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_notification_about_new_registered_user(request, confirmation_user):
    context = {
        'confirmation_user': confirmation_user,
        'domain': get_current_site(request)
    }
    subject = f'HEIs Employers / New Registration'
    message = render_to_string('internships/emails/user_registrated_for_admins.html', context)
    admin_emails = [] 
    for admin_email in User.objects.filter(is_superuser=True).values_list('email'):
        if admin_email[0]:
            admin_emails.append(admin_email[0])
    email = EmailMessage(subject, message, to=admin_emails)
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_resest_password_confirm_email(request, confirmation_user):
    context = {
        'confirmation_user': confirmation_user,
        'domain': get_current_site(request)
    }
    subject = f'HEIs Employers / Reset Password'
    message = render_to_string('internships/emails/user_reset_password.html', context)
    email = EmailMessage(subject, message, to=[confirmation_user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_add_representative_confirm_email(request, confirmation_user):
    context = {
        'confirmation_user': confirmation_user,
        'domain': MAIN_DOMAIN
    }
    subject = f'HEIs Employers / Representative Confirm'
    message = render_to_string('internships/emails/add_representative.html', context)
    email = EmailMessage(subject, message, to=[confirmation_user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_intern_reviewed_by_organization(request, internship_student):
    from .services import get_company_by_user, get_university_by_user
    context = {
        'internship_student': internship_student,
        'domain': MAIN_DOMAIN,
        'company': get_company_by_user(request.user),
        'university': get_university_by_user(request.user)
    }
    subject = f'HEIs Employers / Review'
    message = render_to_string('internships/emails/intern_reviewed_by_organization.html', context)
    email = EmailMessage(subject, message, to=[internship_student.student.user.email])
    email.content_subtype = 'html'
    EmailThread(email).start()


def send_intern_reviewed_by_student(request, internship_student):
    context = {
        'internship_student': internship_student,
        'domain': MAIN_DOMAIN,
        'admin_domain': ADMIN_DOMAIN
    }
    subject = f'HEIs Employers / Review'
    message = render_to_string('internships/emails/admin_intern_reviewed_by_student.html', context)
    admin_emails = [] 
    for admin_email in User.objects.filter(is_superuser=True).values_list('email'):
        if admin_email[0]:
            admin_emails.append(admin_email[0])
    email = EmailMessage(subject, message, to=admin_emails)
    email.content_subtype = 'html'
    EmailThread(email).start()

    subject = f'HEIs Employers / Review'
    message = render_to_string('internships/emails/intern_reviewed_by_student.html', context)
    org_emails = []
    university = internship_student.internship.university
    company = internship_student.internship.company
    org_emails = [
        university.user.email, 
        university.contact_person.email,
        company.user.email,
        company.contact_person.email
    ]
    for staff_users in [university.staff_users.all(), company.staff_users.all()]:
        for staff in staff_users:
            if staff.user.email:
                org_emails.append(staff.user.email)
    email = EmailMessage(subject, message, to=org_emails)
    email.content_subtype = 'html'
    EmailThread(email).start()