from django_extensions.management.jobs import BaseJob


class Job(BaseJob):
    help = "Update battery data from HobbyKing."

    def execute(self):
        from hkbattery.apps.battery.models import run_db_operation
        run_db_operation('update')
        return
