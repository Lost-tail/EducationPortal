from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, include

from internships import views as internships_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
    path('', include('internships.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()


handler400 = 'internships.views.handler_server_error'
handler403 = 'internships.views.handler_server_error'
handler404 = 'internships.views.handler404'
handler500 = 'internships.views.handler_server_error'