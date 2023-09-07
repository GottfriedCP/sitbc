from django.core.management.base import BaseCommand

from sitbc.helper import pop_ind_nl, pop_ind_l


class Command(BaseCommand):
    help = "Populate g sheet from two cspro DB."

    # def add_arguments(self, parser):
    #     parser.add_argument('poll_ids', nargs='+', type=int)

    def handle(self, *args, **options):
        pop_ind_nl(self)
        # pop_ind_l(self)
