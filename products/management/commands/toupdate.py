import csv
import requests
from datetime import date
from products.models import AutomaticProductUpdate
from django.core.management.base import BaseCommand

today = date.today()
url = 'https://productdata.awin.com/datafeed/list/apikey/8ea641145a26285b745ac80a2031b7e1'

class Command(BaseCommand):
    help = "Returns the catalogs which need to be updated today"
    def handle(self, *args, **options):
        update_awin_list = AutomaticProductUpdate.objects.filter(enabled=False)
        update_rest_list = AutomaticProductUpdate.objects.filter(enabled=True)
        with requests.Session() as f:
            download = f.get(url)
            decoded = download.content.decode('utf-8')
            feed = csv.reader(decoded.splitlines(), delimiter=',')
            updates = list(feed)
            for row in updates:
                shop_name = row[1]
                last_update = row[8]
                for conf in update_awin_list:
                    shop = conf.shop
                    if shop == shop_name:
                        if str(today) == last_update[0:10]:
                            conf.update_today = True
                        else:
                            conf.update_today = False

            for conf in update_rest_list:
                last_update = conf.last_update
                if today == last_update:
                    conf.update_today = False
                else:
                    conf.update_today = True


