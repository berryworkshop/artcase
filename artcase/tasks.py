from invoke import run, task

# do the whole shebang:
# $ invoke clean build

@task
def clean(static=True, media=True):
    '''
    Intent: provide a clean slate.
    '''

    patterns = [
        'db.sqlite3',
    ]

    if static:
        patterns.append("../static")
    if media:
        patterns.append("../media")

    for pattern in patterns:
        run("rm -rf {}".format(pattern))

@task
def build(settings='local', images=True):
    '''
    Intent: from a clean slate, get to running again.
    '''

    # basic tasks
    tasks = [
        # gimme static
        "collectstatic",

        # gimme a fresh db
        "migrate",

        # cellini fixtures
        "loaddata artcase/fixtures/categories.yaml",

        # cellini spreadsheets
        "import_csv ../import_data/artifacts.csv",
        "import_csv ../import_data/artists.csv",
        "import_csv ../import_data/glavlit.csv",
        "import_csv ../import_data/printers.csv", 
        "import_csv ../import_data/publishers.csv", 
        "import_csv ../import_data/translations.csv",
    ]
    
    for task in tasks:
        run("./manage.py {} --settings=core.settings.{}".format(task, settings))

    # create dev superuser
    if settings == 'local':
        run('echo "from django.contrib.auth.models import User; User.objects.create_superuser(\'admin\', \'allan.berry@gmail.com\', \'pass\')" | ./manage.py shell  --settings=core.settings.local')

    # import images
    if images:
        run("./manage.py import_images ../import_data/photos_thumb_001-050 --settings=core.settings.{}".format(settings))