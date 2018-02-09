from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg

from products.models import Product


def update_search_vector():
    print("Updating search vector for full text search..")
    vector = SearchVector('name', weight='A') + SearchVector('description', weight='B') + SearchVector('brand',weight='C')
    Product.objects.update(search_vector=vector)
    print("Update complete.")


class Command(BaseCommand):
    help = 'Update search vector for full text search'

    def handle(self, *args, **options):
        update_search_vector()


