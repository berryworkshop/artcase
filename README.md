Build
===

From the artcase directory (same level as ./manage.py):
`$ invoke clean build`


Deploy
===

Deployment is done via Git.

`$ git push`

Publish static files to static server
`$ scp -r ../static allanberry@allanberry.webfactional.com:~/webapps/cellini_static/`

Then you want to ssh to Webfaction, and do other stuff... TODO... probably something like this:
`$ invoke build --settings=production`

CAREFUL: currently the invoke script doesn't care about changes made to the database in production.  So don't make changes on the server and expect them to survive.