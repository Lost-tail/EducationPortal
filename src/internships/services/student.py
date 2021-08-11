from internships.models import StudentSoftSkill, StudentHardSkill

from .services import get_company_by_user, get_university_by_user


def edit_current_student_by_form(request, form_class):
    updated = False
    if request.method == 'POST':
        data = request.POST.dict()
        if data.get('university') == '-1':
            data['university'] = None
        form = form_class(data=data, files=request.FILES, instance=request.user.student)
        if form.is_valid():
            form.save()
            updated = True
    else:
        form = form_class(instance=request.user.student)
    return form, updated


def student_already_applied(student, internship):
    if student.internships_applications.filter(internship=internship):
        return True
    return False


def get_search_student_skills_json(name, skill_type):
    if skill_type == 'soft':
        skill_class = StudentSoftSkill
    elif skill_type == 'hard':
        skill_class = StudentHardSkill
    else:
        return []
    return [
        {'id': skill.id, 'name': skill.name}
        for skill in skill_class.objects.filter(name__istartswith=name)[:6]
    ]


def student_applied_to_organization_by_user(student, user):
    company = get_company_by_user(user)
    if company and company.internships.filter(applications__in=student.internships_applications.all()):
        return True

    university = get_university_by_user(user)
    if university and university.internships.filter(applications__in=student.internships_applications.all()):
        return True

    return False