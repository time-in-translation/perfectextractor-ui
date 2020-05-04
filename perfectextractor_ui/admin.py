from django.contrib import admin
from .models import Corpus


@admin.register(Corpus)
class CorpusAdmin(admin.ModelAdmin):
    pass
