from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url('', include('perfectextractor_ui.urls')),
    url('accounts/', include('django.contrib.auth.urls')),
    url('admin/', admin.site.urls),
]
