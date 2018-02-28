from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg

from products.models import Product


def update_search_vector():
    print("Updating search vector for full text search..")
    vector = SearchVector('name', weight='A')
    # vector = SearchVector('name', weight='A') + SearchVector('description', weight='C') + SearchVector('brand',weight='D')
    # vector = SearchVector('name', config='spanish', weight='A') + SearchVector('description', config='spanish',
    #                                                                            weight='C') + SearchVector('brand',
    #                                                                                                       config='spanish',
    #                                                                                                       weight='D')
    Product.objects.update(search_vector=vector)
    print("Update complete.")


class Command(BaseCommand):
    help = 'Update search vector for full text search'

    def handle(self, *args, **options):
        update_search_vector()


