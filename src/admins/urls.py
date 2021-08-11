from django.urls import path

from . import views


urlpatterns = [
    path('', views.internships_list_view, name='internships_list'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('internship/create', views.internship_create_view, name='internship_create'),
    path('internship/<int:pk>/edit', views.internship_edit_view, name='internship_edit'),
    path('internship/<int:pk>/delete', views.internship_delete_view, name='internship_delete'),
    path('internship/<int:internship_pk>/applications', views.internship_applications_list_view, name='internship_applications_list'),
    path('internship-application/<int:pk>/edit', views.internship_applications_edit_view, name='internship_application_edit'),
    path('internship-application/<int:pk>/delete', views.internship_application_delete_view, name='internship_application_delete'),
    path('internship/<int:internship_pk>/interns', views.internship_interns_list_view, name='internship_interns_list'),
    path('intern/<int:pk>/edit', views.internship_student_edit_view, name='internship_student_edit'),
    path('intern/<int:pk>/delete', views.internship_student_delete_view, name='internship_student_delete'),
    path('universities', views.universities_list_view, name='universities_list'),
    path('university/<int:pk>/edit', views.university_edit_view, name='university_edit'),
    path('university/<int:pk>/delete', views.university_delete_view, name='university_delete'),
    path('companies', views.companies_list_view, name='companies_list'),
    path('company/<int:pk>/edit', views.company_edit_view, name='company_edit'),
    path('company/<int:pk>/delete', views.company_delete_view, name='company_delete'),
    path('staff', views.staff_users_list_view, name='staff_users_list'),
    path('staff/<int:pk>/edit', views.staff_user_edit_view, name='staff_user_edit'),
    path('staff/<int:pk>/delete', views.staff_user_delete_view, name='staff_user_delete'),
    path('countries', views.countries_list_view, name='countries_list'),
    path('country/<int:pk>/edit', views.country_edit_view, name='country_edit'),
    path('country/<int:pk>/delete', views.country_delete_view, name='country_delete'),
    path('students', views.students_list_view, name='students_list'),
    path('student/<int:pk>/edit', views.student_edit_view, name='student_edit'),
    path('student/<int:pk>/delete', views.student_delete_view, name='student_delete'),
    path('languages', views.languages_list_view, name='languages_list'),
    path('language/<int:pk>/edit', views.language_edit_view, name='language_edit'),
    path('language/<int:pk>/delete', views.language_delete_view, name='language_delete')
]