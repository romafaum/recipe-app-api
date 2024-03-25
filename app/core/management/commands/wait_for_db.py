import time
from typing import Any
from psycopg import OperationalError as PsycopgOpError
from django.db.utils import OperationalError
from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        self.stdout.write('Waiting for database...')
        db_up = False
        while db_up is False:
            try:
                self.check(databases=['default'])
                db_up = True
            except (PsycopgOpError, OperationalError):
                self.stdout.write('Database unvailable, wait for 1 second ...')
                time.sleep(1)
        self.stdout.write(self.style.SUCCESS('Successful connection to databases!')) # noqa
