from django.db import models
from ckeditor.fields import RichTextField
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
        ordering = ["title_english", "code_number"]

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

    def edition(self):
        # quck way to print edition of artifact
        return "{0} / {1}".format(self.edition_state, str(self.edition_size))
    edition_state = models.CharField(max_length = 100,
        default='1', blank = True, null = True)
    edition_size  = models.IntegerField(blank = True, null = True,
        default=1)

    code_number = models.CharField('Code Number',
        max_length = 10, unique = True)
    public = models.BooleanField('Public or Private', choices=PUBLIC_CHOICES,
        default = True)
    title_english = models.CharField(max_length = 100,
        default = 'Untitled', blank=False, null=False)
    title_russian = models.CharField(max_length = 100,
        default = 'Без названия', blank=True, null=True)
    description = RichTextField(max_length = 10000, blank = True,
        config_name="basic_ckeditor")

    SUPPORTS = (
        ('paper', 'paper'),
        ('panel', 'panel'),
        ('canvas', 'canvas'),
    )
    support   = models.CharField(max_length = 100,
        choices=SUPPORTS, blank=True, default="paper")

    def __unicode__(self):
        return self.code_number + ": " + self.title_english
    def natural_key(self):
        return (self.code_number,)  # must return a tuple
    def get_absolute_url(self):
        #return "/collection/artifacts/{}/".format(self.code_number)
        pass