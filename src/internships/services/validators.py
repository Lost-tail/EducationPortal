from django.core.exceptions import ValidationError
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


def clean_internship_applications_deadline(internship_form):
    applications_deadline = internship_form.cleaned_data['applications_deadline']
    start_date = internship_form.cleaned_data['start_date']
    if applications_deadline <= timezone.now().date():
        internship_form.add_error(
            'applications_deadline', _('The date must be greater than to the current date.')
        )
    if applications_deadline >= start_date:
        internship_form.add_error(
            'applications_deadline', _('Call Deadline Date must be less than the Initial Date.')
        )


def clean_internship_start_date(internship_form):
    start_date = internship_form.cleaned_data['start_date']
    end_date = internship_form.cleaned_data['end_date']
    if start_date >= end_date:
        internship_form.add_error('start_date', _('Initial Date must be less than End Date.'))


def file_max_10mb_size(value): # add this to some file where you can import it from
    limit = 10 * 1024 * 1024
    if value.size > limit:
        raise ValidationError(_('The maximum file size that can be uploaded is 10MB.'))