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
        self.start_webpack()
        return super(Command, self).inner_run(*args, **options)

    def start_webpack(self):
        self.stdout.write('>>> Starting webpack')
        self.webpack_process = subprocess.Popen(
            ['cd .. && webpack --watch'],
            shell=True,
            stdin=subprocess.PIPE,
            stdout=self.stdout,
            stderr=self.stderr,
        )

        self.stdout.write('>>> webpack process on pid {0}'.format(self.webpack_process.pid))

        def kill_webpack_process(pid):
            self.stdout.write('>>> Closing webpack process')
            os.kill(pid, signal.SIGTERM)

        atexit.register(kill_webpack_process, self.webpack_process.pid)