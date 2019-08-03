from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import (
    include,
    path,
)
from django.utils.translation import ugettext_lazy as _

admin.site.site_header = _('Izyan Poker')
admin.site.site_title = _('Izyan Poker')

urlpatterns = [
    path('', include('apps.poker.urls', namespace='poker')),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
