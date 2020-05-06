from django.core.management.base import BaseCommand, CommandError
from loan.models import Session
import datetime

class Command(BaseCommand):
    help = 'Closes the specified poll for voting'

    def handle(self, *arguments, **options):

        session = Session.get_active_session()

        if session is None:
            return

        last_update = session.last_action_time
        now = datetime.datetime.now()

        time_delta = now - last_update

        if time_delta.total_seconds() > 5:
            session.timeout()
            session.save()


