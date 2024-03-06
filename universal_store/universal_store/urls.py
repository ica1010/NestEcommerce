from django import views
from django.contrib import admin
from django.urls import include, path
from django.conf.urls.i18n import i18n_patterns

from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.utils.translation import gettext_lazy as _
import notifications.urls
from core.views import *

urlpatterns = [
    path('selectlanguage/', selectlanguage, name='selectlanguage'),
    path('selectcurrency/', selectcurrency, name='selectcurrency'),
    path('savelangcur/', savelangcur, name='savelangcur'),
    path('i18n/', include('django.conf.urls.i18n')),

]

urlpatterns += i18n_patterns(
    path('currencies/', include('currencies.urls')),
    path(_('admin/'), admin.site.urls),
    path('administator/', include('admin_soft.urls')),
    path(_(''), include('core.urls')),
    path(_('user/'), include('userauths.urls')),
    path('user/', include('allauth.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('notifications/', include(notifications.urls, namespace='notifications')),
    # path('i18n/', include('django.conf.urls.i18n')),
    prefix_default_language=False,
    )

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
