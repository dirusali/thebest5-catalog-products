#!/bin/bash

source /home/ubuntu/.venv/bin/activate
exec /home/ubuntu/.venv/bin/gunicorn --timeout 1200 --graceful-timeout 60  --workers 9 --bind unix:/home/ubuntu/thebest5-catalog-products/best5_catalog.sock thebest5_catalog_products.wsgi:application

