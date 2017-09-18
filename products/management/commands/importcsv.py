import os
import csv

from django.core.management.base import BaseCommand, CommandError
from products.models import Product, Shop, convert_header

class Command(BaseCommand):
    help = 'Import a csv into `Product` database.'

    def add_arguments(self, parser):
        # Positional arguments
        parser.add_argument('csv_file')
    

    def handle(self, *args, **options):
        if len(args) != 1:
            raise CommandError ("Invalid Invocation. See help.")

        csvPath = args[0]
        shop = Shop.objects.get(pk=1)
        if not os.path.exists (csvPath):
            raise CommandError ("%s doesnt exist." %csvPath)
        
        model_fields = [f.name for f in Model._meta.fields]
        self.stdout.write("begin process...")        
        with open (csvPath, 'rb') as csv_file:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=';')
            header_ = next(reader)
            header_cols = convert_header(header_)
            for row in reader:
                try:
                    obj = Product()
                    obj.shop = shop
                    for i, field in enumerate(row):
                        setattr(obj, header_cols[i], field)
                    obj.save()
                except:
                    pass
                    

        self.stdout.write("finish process...")        
