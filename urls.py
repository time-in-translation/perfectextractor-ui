from django.conf.urls import include, url

urlpatterns = [
    url('', include('perfectextractor_ui.urls')),
    url('accounts/', include('django.contrib.auth.urls')),
]
