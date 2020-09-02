import json
import os
from django.conf import settings
from django.db import models


class Task(models.Model):
    outfile = models.CharField(max_length=255)
    status_json = models.CharField(default='{}', max_length=255)
    started = models.DateTimeField(auto_now_add=True)

    @property
    def status(self):
        return json.loads(self.status_json)

    @status.setter
    def status(self, value):
        self.status_json = json.dumps(value)


class Corpus(models.Model):
    title = models.CharField(max_length=100)
    path = models.FilePathField(path=settings.PE_DATA_PATH,
                                recursive=True,
                                allow_folders=True,
                                allow_files=False)
    is_public = models.BooleanField()
    source_format = models.CharField(max_length=100,
                                     choices=[('opus', 'opus'),
                                              ('bnc', 'bnc'),
                                              ('dpc', 'dpc')])

    class Meta:
        verbose_name_plural = 'Corpora'

    def __str__(self):
        return self.title

    @property
    def sources(self):
        sources = []
        try:
            for d in os.listdir(self.path):
                if os.path.isdir(os.path.join(self.path, d)):
                    sources.append(d)
        except FileNotFoundError:
            pass

        return sorted(sources)

    def list_documents(self, language):
        docs = []
        if os.path.exists(os.path.join(self.path, language)):
            for f in os.listdir(os.path.join(self.path, language)):
                docs.append(f)

        return sorted(docs)
