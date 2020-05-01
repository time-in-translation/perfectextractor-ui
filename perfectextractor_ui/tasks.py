from django import db
from multiprocessing import Process

from .models import Task


class TaskProcess:
    def __init__(self, task_id, target, args):
        self._task_id = task_id
        self._target = target
        self._args = args

    def start(self):
        self._process = Process(target=self._run)
        self._process.start()

    def cancel(self):
        self._process.kill()

    def is_alive(self):
        return self._process.is_alive()

    def _run(self):
        self._target(self._cb, *self._args)

    def _cb(self, status):
        # when using mysql, we need to reconnect because this is running in a new process
        db.close_old_connections()
        t = Task.objects.get(pk=self._task_id)
        t.status = status
        t.save()


class TaskController:
    def __init__(self):
        self._processes = {}

    def add(self, func, args):
        t = Task.objects.create()
        t.save()
        p = TaskProcess(t.pk, func, args)
        self._processes[t.pk] = p
        p.start()
        return t.pk

    def monitor(self, task_id):
        t = Task.objects.get(pk=task_id)
        return t.status

    def cancel(self, task_id):
        self._processes[task_id].cancel()


tasks = TaskController()
