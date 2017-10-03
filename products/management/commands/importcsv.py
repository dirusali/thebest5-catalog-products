import os
import csv
import io
import mmap
from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Shop
from tqdm import tqdm

def get_num_lines(file_path):
    fp = open(file_path, "r+")
    buf = mmap.mmap(fp.fileno(), 0)
    #initialize lines (counter) with -1 to subtract the header
    lines = -1
    while buf.readline():
        lines += 1
    return lines

def isfloat(value):
  try:
    float(value)
    return True
  except:
    return False

# This dictionary contains specific headers conversions for each Shop.
map_columns = {
    #Admitad products: BestGear, TOMTOP, Banggood
    'id':'product_id',
    'picture':'image',
    'currencyid':'currency',
    'oldprice':'old_price',
    #PC Components
    'sku':'product_id',
    'url_product':'url',
    'url_image':'image',
    'pricenorebate':'old_price',
    #FNAC
    'tdproductid':'product_id',
    'producturl':'url',
    'imageurl':'image',
    'currencyid':'currency',
    'previousprice':'old_price',
    'shippingcost':'shipping_cost',
}

def convert_header(csv_header):
    """ This funcion converts a word header to the convenient for our Product model """
    header_ = csv_header
    cols = []
    for i, h in enumerate(header_):
        col = h.replace(' ', '_').lower()
        try:
            header_[i] = map_columns[col]
        except KeyError:
            header_[i] = col
    return header_

class Command(BaseCommand):
    help = 'Import a csv into `Product` database.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('path')
        # Named (optional) arguments
        parser.add_argument(
            '--shop-id',
            dest='shop_id',
            help='The Shop id. Raise error if not exists.',
        )        

        parser.add_argument(
            '--csv-column-delimiter',
            dest='column_delimiter',
            default=';',
            help='Column delimiter to parse the csv file. By default it is semicolon',
        )        
        
        
        parser.add_argument(
            '--shop-name',
            dest='shop_name',
            help='Get or create a new Shop with name passed as argument',
        )

        parser.add_argument(
            '--no-delete-products',
            action='store_true',
            dest='no_delete_products',
            default=False,
            help='By default the process delete all the previous existing products for the shop given as argument. If --no-delete-products is given, the command will no delete any product before the insert',
        )
        
    def handle(self, *args, **options):
        file_path = options['path']
        if options['shop_name']:
            shop, created = Shop.objects.get_or_create(name=options['shop_name'])
        if options['shop_id']:
            shop_id = options['shop_id']
            try:
                shop = Shop.objects.get(pk=shop_id)
            except Shop.DoesNotExist:
                raise CommandError ("Shop with Id %s doesnt exist." % shop_id)
        
        if not os.path.exists(file_path):
            raise CommandError ("The file %s doesnt exist." % file_path)

        products_count = Product.objects.filter(shop=shop).count()
        self.stdout.write("There are %d existing products for the shop %s ... " % (products_count, shop.name))
        if not options['no_delete_products']:
            #first delete all existing products.
            self.stdout.write("Delete previously existing products for shop %s ... " % shop.name)
            Product.objects.filter(shop=shop).delete()
            self.stdout.write("Delete previously existing products for shop %s ... DONE " % shop.name)
            self.stdout.write("-------------------------------------------------------- ")
        
        self.stdout.write("Begin process of import products to shop %s " % shop.name)
        self.stdout.write("Column delimiter to use is %s ..." % options['column_delimiter'])
        with open(file_path, 'rb') as file:
            decoded_file = file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=options['column_delimiter'])
            header_ = next(reader)
            header_cols = convert_header(header_)
            for row in tqdm(reader, total=get_num_lines(file_path)):
                try:
                    obj = Product()
                    obj.shop = shop
                    for i, field in enumerate(row):
                        if header_cols[i] == 'price' or header_cols[i] == 'old_price':
                            if not isfloat(field):
                                field = None
                        setattr(obj, header_cols[i], field)
                    obj.save()
                except:
                    self.stdout.write(options['column_delimiter'].join(row))
        self.stdout.write("Process finished!")

