Collect static files
---

`./manage.py collectstatic --settings=core.settings.local`


Start server (localhost):
---

`./manage.py runserver 0.0.0.0:1917 --settings=core.settings.local`

Reset db
---

`rm db.sqlite3`
`./manage.py migrate --settings=core.settings.local`
`./manage.py loaddata artcase/fixtures/categories.yaml --settings=core.settings.local`

`./manage.py import_csv ../import_data/artifacts.csv --settings=core.settings.local`
`./manage.py import_csv ../import_data/artists.csv --settings=core.settings.local`
`./manage.py import_csv ../import_data/glavlit.csv --settings=core.settings.local`
`./manage.py import_csv ../import_data/printers.csv --settings=core.settings.local`
`./manage.py import_csv ../import_data/publishers.csv --settings=core.settings.local`
`./manage.py import_csv ../import_data/translations.csv --settings=core.settings.local`

`./manage.py createsuperuser --username=niteshade --email=allan.berry@gmail.com --settings=core.settings.local`


Import images
---

`./manage.py import_images ../import_data/photos_thumb_001-050 --settings=core.settings.local`



Deployment
===

After collectstatic (above), publish static files to static server

`scp -r ../static allanberry@allanberry.webfactional.com:~/webapps/cellini_static/`