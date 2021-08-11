from django.contrib import admin


from .models import *


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    pass


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    pass


@admin.register(ContactPerson)
class ContactPersonAdmin(admin.ModelAdmin):
    pass


class StudentEducationInline(admin.TabularInline):
    model = StudentEducation
    extra = 0


class StudentWorkInline(admin.TabularInline):
    model = StudentWork
    extra = 0


class StudentPublicationInline(admin.TabularInline):
    model = StudentPublication
    extra = 0


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    inlines = [StudentEducationInline, StudentWorkInline, StudentPublicationInline]


@admin.register(StudentSoftSkill)
class StudentSoftSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentHardSkill)
class StudentHardSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(StudentEducationAcquiredSkill)
class StudentEducationAcquiredSkillAdmin(admin.ModelAdmin):
    pass


@admin.register(University)
class UniversityAdmin(admin.ModelAdmin):
    pass


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


class InternshipStudentInline(admin.TabularInline):
    model = InternshipStudent
    extra = 0


@admin.register(Internship)
class InternshipAdmin(admin.ModelAdmin):
    inlines = [InternshipStudentInline]


@admin.register(InternshipStudent)
class InternshipStudentAdmin(admin.ModelAdmin):
    pass    


@admin.register(InternshipApplication)
class InternshipApplicationAdmin(admin.ModelAdmin):
    pass


@admin.register(InternshipReview)
class InternshipReviewAdmin(admin.ModelAdmin):
    pass


@admin.register(InternshipFile)
class InternshipFileAdmin(admin.ModelAdmin):
    pass


@admin.register(StaffUser)
class StaffUserAdmin(admin.ModelAdmin):
    pass


@admin.register(UserConfirmation)
class UserConfirmationAdmin(admin.ModelAdmin):
    pass