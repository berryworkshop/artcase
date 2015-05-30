from django.db import models
from .constants import LANGUAGES, PUBLIC_CHOICES


class ArtifactManager(models.Manager):
    '''
        Refer to an artifact by a meaningful name: its slug.
    '''
    def get_by_natural_key(self, code_number_):
        return self.get(code_number=code_number_)

class Artifact(models.Model):
    '''
        Artifacts are the main object tracked by the site.  One artifact
        essentially equals one cataloged artwork: one entity.  In this case,
        usually a poster.
    '''

    class Meta:
        ordering = ["title_roman", "code_number"]

    objects = ArtifactManager()

    #artists   = models.ManyToManyField('Artist', blank = True)
    #cultures  = models.ManyToManyField('Culture', blank = True)
    #media     = models.ManyToManyField('Medium', blank = True)
    #subjects  = models.ManyToManyField('Subject', blank = True)

    #category  = models.ForeignKey('Category', blank = False,
    #    null = False, default=0)
    #publisher = models.ForeignKey('Organization',
    #    related_name='artifacts_published', blank = True, null = True)
    #printer   = models.ForeignKey('Organization',
    #    related_name='artifacts_printed',   blank = True, null = True)

    code_number = models.SlugField(
        'Code Number', unique=True, blank=False)
    title_roman = models.CharField(
        max_length = 255, default='Untitled', blank=False)
    title_cyrillic = models.CharField(
        max_length = 255, default='Без названия')
    description = models.TextField(max_length=100000)

    edition_state = models.CharField(max_length=255, default='1')
    edition_size  = models.CharField(max_length=255, default='1')

    public = models.BooleanField(
        'Public or Private', choices=PUBLIC_CHOICES, default = False)

    SUPPORTS = (
        ('paper', 'paper'),
        ('panel', 'panel'),
        ('canvas', 'canvas'),
    )
    support   = models.CharField(
        max_length = 100, choices=SUPPORTS, blank=True, default="paper")

    def __unicode__(self):
        return self.code_number + ": " + self.title_roman
    def natural_key(self):
        return (self.code_number,)  # must return a tuple
    def get_absolute_url(self):
        return "/collection/artifacts/{}/".format(self.code_number)

    def edition(self):
        return "{0} / {1}".format(self.edition_state, str(self.edition_size))