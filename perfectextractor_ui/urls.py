from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from django.views.generic.base import TemplateView

from . import views

app_name = 'perfectextractor_ui'
urlpatterns = [
    path('', views.home, name='home'),
    path('run', views.run, name='run'),
    path('status/<int:task_id>', views.status, name='status'),
    path('peek/<int:task_id>', views.peek, name='peek'),
    path('cancel/<int:task_id>', views.cancel, name='cancel'),
    path('download/<int:task_id>', views.download, name='download'),
    path('import_query', views.import_query, name='import_query'),
    path('help', views.help, name='help'),
] + static('/static/', document_root=settings.STATIC_ROOT)
