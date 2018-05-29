import csv
import os
import shutil
import zipfile
import requests
from datetime import date
from datetime import datetime
from urllib.request import URLopener
from django.core.management.base import BaseCommand
from products.management.commands.importcsv import load_catalog_to_db
from products.management.commands.update_search_vector import update_search_vector
from products.models import AutomaticProductUpdate
from thebest5_catalog_products.settings import CATALOGS_ROOT

today = date.today()
url = 'https://productdata.awin.com/datafeed/list/apikey/8ea641145a26285b745ac80a2031b7e1'
awin = AutomaticProductUpdate.objects.filter(enabled=False)
rest = AutomaticProductUpdate.objects.filter(enabled=True)
lista = list()

with requests.Session() as f:
    download = f.get(url)
    decoded = download.content.decode('utf-8')
    feed = csv.reader(decoded.splitlines(), delimiter=',')
    updates = list(feed)
    for row in updates:
        shop_name = row[1]
        last_update = row[8]
        for conf in awin:
            if shop_name == conf.shop:
                if str(today) == last_update[0:10]:
                    lista.append(conf)
                else:
                    print ("no updates pending in awin")

for conf in rest:
    last_update = conf.last_update
    if today == last_update:
        pass
    else:
        lista.append(conf)


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
        for catalogo in lista:
            shop_name = catalogo.shop
            print("Updating catalog for shop '%s'.." % shop_name)
            print("-------------------------------------------------------- ")
            try:
                print("Dowloading catalog file for shop '%s', from url:%s" % (shop_name, catalogo.catalog_url))
                file = URLopener()
                if not os.path.exists(CATALOGS_ROOT):
                    os.makedirs(CATALOGS_ROOT)
                catalog_filename = CATALOGS_ROOT+'/%s_catalog' % shop_name
                if catalogo.is_compressed:
                    extension = '.%s' % catalogo.compress_format
                else:
                    extension = '.csv'
                catalog_filename += extension
                file.retrieve(catalogo.catalog_url, catalog_filename)
                print("Catalog file retrieved for shop '%s', local path:%s" % (shop_name, catalog_filename))
                if catalogo.is_compressed:
                    print("Decompressing file ...")
                    # Get a new clean tmp dir
                    tmp_dir = CATALOGS_ROOT + '/%s_tmp' % shop_name
                    if os.path.exists(tmp_dir):
                        shutil.rmtree(tmp_dir)
                    os.makedirs(tmp_dir)
                    # Extract catalog (should be a single file inside compressed file)
                    if not decompress_file(input_file=catalog_filename,
                                           output_dir=tmp_dir,
                                           compression_format=catalogo.compress_format):
                        print("Decompressing file ... ERROR")
                        return -1
                    # Copy and rename the extracted catalog file
                    extracted_catalog = os.listdir(tmp_dir)[0]
                    catalog_filename = catalog_filename[:-4] + ".csv"
                    extracted_catalog_path = os.path.abspath(os.path.join(tmp_dir, extracted_catalog))
                    shutil.copyfile(extracted_catalog_path, catalog_filename)
                    print("Decompressing file ... DONE")
                print("Import products from file to DB ...")
                records_num = load_catalog_to_db(shop=catalogo.shop,
                                   catalog_path=catalog_filename,
                                   delimiter=catalogo.delimiter,
                                   delete_products=True,
                                   print_errors=False)
                catalogo.last_update = datetime.now()
                catalogo.local_file = catalog_filename
                catalogo.records_num = records_num
                catalogo.save()
                print("Import products from file to DB ... DONE")
            except Exception as e:
                print("ERROR Importing updating catalog for shop %s [SKIPPED]\n%s" %(shop_name, e))
        else:
            print("-------------------------------------------------------- ")

        print("All catalogs processed.")
        update_search_vector()
        print("Catalogs update complete.")
