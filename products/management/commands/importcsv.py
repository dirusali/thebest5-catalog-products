import os
import csv
import io
import mmap
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Shop, convert_header
from tqdm import tqdm

def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    #initialize lines (counter) with -1 to subtract the header
    lines = -1
    while buf.readline():
        lines += 1
    return lines

class Command(BaseCommand):
    help = 'Import a csv into `Product` database.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path')
        parser.add_argument('shop_id')
    

    def handle(self, *args, **options):
        file_path = options['path']
        shop_id = options['shop_id']
        try:
            shop = Shop.objects.get(pk=shop_id)
        except Shop.DoesNotExist:
            raise CommandError ("Shop with Id %s doesnt exist." % shop_id)
        
        if not os.path.exists(file_path):
            raise CommandError ("The file %s doesnt exist." % file_path)
        
        self.stdout.write("Begin process of import products ...")
        with open(file_path, 'rb') as file:
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=';')
            header_ = next(reader)
            header_cols = convert_header(header_)
            for row in tqdm(reader, total=get_num_lines(file_path)):
                try:
                    obj = Product()
                    obj.shop = shop
                    for i, field in enumerate(row):
                        setattr(obj, header_cols[i], field)
                    obj.save()
                except:
                    pass
        self.stdout.write("Finish process...")
