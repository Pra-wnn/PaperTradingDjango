from django.apps import AppConfig


class ApiConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'api'


    # # after you made signals.py just need to speicify here to make it work
    def ready(self):
        # from api.signals import update_balance
        from api.signals import update_balances
        from api.signals import create_related_instances
        # remeber to import specidi not jsut signals
