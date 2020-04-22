import json
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
