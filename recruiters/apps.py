from django.apps import AppConfig


class RecruitersConfig(AppConfig):
    name = 'recruiters'

    def ready(self):
        import recruiters.signals