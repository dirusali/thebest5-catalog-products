import os
import shutil
import zipfile
from datetime import datetime
from urllib.request import URLopener
from django.core.management.base import BaseCommand
from products.management.commands.importcsv import load_catalog_to_db
from products.management.commands.update_search_vector import update_search_vector
from products.models import AutomaticProductUpdate
from products.models import Product
from thebest5_catalog_products.settings import CATALOGS_ROOT
from postgres_copy import CopyManager


def decompress_file(input_file, output_dir, compression_format):
    if compression_format.lower() == 'zip':
        zip_ref = zipfile.ZipFile(input_file, 'r')
        zip_ref.extractall(output_dir)
        zip_ref.close()
        return True
    return False


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
                    extension = '.%s' % conf.compress_format
                else:
                    extension = '.csv'
                catalog_filename += extension
                file.retrieve(conf.catalog_url, catalog_filename)
                print("Catalog file retrieved for shop '%s', local path:%s" % (shop_name, catalog_filename))
                if conf.is_compressed:
                    print("Decompressing file ...")
                    # Get a new clean tmp dir
                    tmp_dir = CATALOGS_ROOT + '/%s_tmp' % shop_name
                    if os.path.exists(tmp_dir):
                        shutil.rmtree(tmp_dir)
                    os.makedirs(tmp_dir)
                    # Extract catalog (should be a single file inside compressed file)
                    if not decompress_file(input_file=catalog_filename,
                                           output_dir=tmp_dir,
                                           compression_format=conf.compress_format):
                        print("Decompressing file ... ERROR")
                        return -1
                    # Copy and rename the extracted catalog file
                    extracted_catalog = os.listdir(tmp_dir)[0]
                    catalog_filename = catalog_filename[:-4] + ".csv"
                    extracted_catalog_path = os.path.abspath(os.path.join(tmp_dir, extracted_catalog))
                    shutil.copyfile(extracted_catalog_path, catalog_filename)
                    print("Decompressing file ... DONE")
                print("Import products from file to DB ...")
                records_num = Product.objects.from_csv(extracted_catalog_path, delimiter = conf.delimiter)
                conf.last_update = datetime.now()
                conf.local_file = catalog_filename
                conf.records_num = records_num
                conf.save()
                print("Import products from file to DB ... DONE")
            except Exception as e:
                print("ERROR Importing updating catalog for shop %s [SKIPPED]\n%s" %(shop_name, e))
                continue
            print("-------------------------------------------------------- ")
        print("All catalogs processed.")
        

