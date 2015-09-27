Build
===

From the artcase directory (same level as ./manage.py):
`$ invoke clean build`


Deploy
===

Publish static files to static server
`$ scp -r ../static allanberry@allanberry.webfactional.com:~/webapps/cellini_static/`