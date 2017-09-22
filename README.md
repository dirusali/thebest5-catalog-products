# Custom product feed service for catalog products taken from admitad and others #

## Managment command to import CSV catalog: ##

`python manage.py importcsv products_405091641.csv --shop-name 'PC Components'`

This will create a new Shop with name "PC Components" and then import
each product of the catalog. By default the command will delete all of
the previous products for the shop given as parameter.

If for some reason, you do not want to delete the previously imported
products, you need to add the argument *--no-delete-products*:
`python manage.py importcsv products_405091641.csv --shop-name 'PC Components' --no-delete-products`

Also you can use the Id or Pk instead of the name of the shop:
`python manage.py importcsv products_405091641.csv --shop-id 2`

This will import each product of the catalog to the shop with the ID given as parameter.

See python manage.py importcsv -h for help.






