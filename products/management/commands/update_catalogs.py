import os
from urllib.request import URLopener

from datetime import datetime
from django.core.management.base import BaseCommand, CommandError
from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank
from django.contrib.postgres.aggregates import StringAgg

from products.management.commands.importcsv import load_catalog_to_db
from products.management.commands.update_search_vector import update_search_vector
from products.models import Product, AutomaticProductUpdate
from subprocess import call

from thebest5_catalog_products.settings import VENV_PYTHON, CATALOGS_ROOT


class Command(BaseCommand):
    help = "Downloads the last catalogs for each shop and updates 'Product' database."

    def handle(self, *args, **options):
        print("Updating catalogs..")
        update_conf_list = AutomaticProductUpdate.objects.filter(enabled=True)
        for conf in update_conf_list:
            shop_name = conf.shop
            print("Updating catalog for shop '%s'.." % shop_name)
            print("-------------------------------------------------------- ")
            try:
                print("Dowloading catalog file for shop '%s', from url:%s" % (shop_name, conf.catalog_url))
                file = URLopener()
                if not os.path.exists(CATALOGS_ROOT):
                    os.makedirs(CATALOGS_ROOT)
                catalog_filename = CATALOGS_ROOT+'/%s_catalog' % shop_name
                if conf.is_compressed:
                    extension = conf.compress_format
                else:
                    extension = '.csv'
                catalog_filename += extension
                file.retrieve(conf.catalog_url, catalog_filename)
                print("Catalog file retrieved for shop '%s', local path:%s" % (shop_name, catalog_filename))
                if conf.is_compressed:
                    print("COMPRESSION NOT SUPPORTED YET! ABORT.")
                    return
                print("Import products from file to DB ...")
                load_catalog_to_db(shop=conf.shop,
                                   catalog_path=catalog_filename,
                                   delimiter=conf.delimiter,
                                   delete_products=True,
                                   print_errors=False)
                conf.last_update = datetime.now()
                conf.local_file = catalog_filename
                conf.save()
                print("Import products from file to DB ... DONE")
            except Exception as e:
                print("ERROR Importing updating catalog for shop %s [SKIPPED]\n%s" %(shop_name, e))
                continue
            print("-------------------------------------------------------- ")
        print("All catalogs processed.")
        update_search_vector()
        print("Catalogs update complete.")

