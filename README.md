Collect static files

* ./manage.py collectstatic --settings=core.settings.local


Start server (localhost):

* ./manage.py runserver 0.0.0.0:1917 --settings=core.settings.local


To import starter data (not in .json files):

* ./manage.py import_csv ../import_data/artifacts.csv
* ./manage.py import_csv ../import_data/artists.csv
* ./manage.py import_csv ../import_data/glavlit.csv
* ./manage.py import_csv ../import_data/printers.csv
* ./manage.py import_csv ../import_data/publishers.csv
* ./manage.py import_csv ../import_data/translations.csv