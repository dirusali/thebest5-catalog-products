from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg

from products.models import Product


class Command(BaseCommand):
    help = 'Import a csv into `Product` database.'

    def handle(self, *args, **options):
        print("Updating search vector for full text search..")
        vector = SearchVector('name', weight='A') + \
                 SearchVector('description', weight='B')
        Product.objects.update(search_vector=vector)
        print("Update complete.")

