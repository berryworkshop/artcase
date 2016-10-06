import os
import subprocess
import atexit
import signal

from django.conf import settings
from django.contrib.staticfiles.management.commands.runserver import Command\
    as StaticfilesRunserverCommand

# hat tip:
# https://lincolnloop.com/blog/simplifying-your-django-frontend-tasks-grunt/
# https://lincolnloop.com/blog/integrating-front-end-tools-your-django-project/


class Command(StaticfilesRunserverCommand):
    def inner_run(self, *args, **options):
        self.start_gulp()
        return super(Command, self).inner_run(*args, **options)

    def start_gulp(self):
        self.stdout.write('>>> Starting gulp')
        self.gulp_process = subprocess.Popen(
            ['gulp watch'],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write('>>> Gulp process on pid {0}'.format(self.gulp_process.pid))

        def kill_gulp_process(pid):
            self.stdout.write('>>> Closing gulp process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_gulp_process, self.gulp_process.pid)