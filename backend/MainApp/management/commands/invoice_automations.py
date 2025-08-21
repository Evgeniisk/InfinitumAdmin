#The BaseCommand Django class is used to make custom management comands which can be called with python manage.py 
from django.core.management.base import BaseCommand
from MainApp.cron import InvoicesAutomationsTiedtoContract, InvoicesAutomationsNotTiedtoContract
#This command is used for testing cron jobs and calling them using django cron tabs module configurations in settings
class Command(BaseCommand):
    help = 'Run to test cron jobs'

    def handle(self, *args, **kwargs):
        InvoicesAutomationsTiedtoContract()
        InvoicesAutomationsNotTiedtoContract()