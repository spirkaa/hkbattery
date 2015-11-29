from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "Update battery data from HobbyKing and exchange rate"

    def execute(self):
        from hkbattery.apps.battery.models import ExchRate, run_db_operation
        from hkbattery.apps.battery.utils import exchange_rate
        ExchRate.objects.update_or_create(
            pk=1,
            defaults={'ex_rate': exchange_rate('EUR', 'RUB')})
        run_db_operation('update')
        return
