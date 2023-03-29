from django.apps import AppConfig


class LibsysConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'LIBSYS'

    def ready(self):
        # pass
        from jobs import updater
        updater.start()
        # from .runapscheduler import Command, my_job
        # # job = Command()
        # job.handle()
