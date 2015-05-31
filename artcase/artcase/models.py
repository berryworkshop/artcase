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
        ordering = ["title_english", "code_number"]

    objects = ArtifactManager()

    creators   = models.ManyToManyField('Creator', blank = True)
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
    title_english = models.CharField(
        max_length = 255, default='Untitled', blank=False)
    title_original = models.CharField(
        max_length = 255, default='Без названия', blank=True)
    description = models.TextField(max_length=100000, blank=True)

    edition_state = models.CharField(max_length=255, default='1', blank=True)
    edition_size  = models.CharField(max_length=255, default='1', blank=True)

    public = models.BooleanField(
        'Public or Private', choices=PUBLIC_CHOICES, default=False, blank=False)

    SUPPORTS = (
        ('paper', 'paper'),
        ('panel', 'panel'),
        ('canvas', 'canvas'),
    )
    support   = models.CharField(
        max_length = 100, choices=SUPPORTS, default="paper", blank=True)

    def __str__(self):
        return self.code_number + ": " + self.title_english
    def natural_key(self):
        return (self.code_number,)  # must return a tuple
    def get_absolute_url(self):
        return "/collection/artifacts/{}/".format(self.code_number)

    def edition(self):
        return "{0} / {1}".format(self.edition_state, str(self.edition_size))

class Creator(models.Model):
    '''
        Any creator who had a hand in making an artifact.
    '''

    slug = models.SlugField(unique=True, blank=False)
    name_latin_last  = models.CharField(
        "Last Name (Latin Alphabet)", max_length = 100, blank=False)
    name_latin_first = models.CharField(
        "First Name (Latin Alphabet)", max_length = 100, blank=True)
    name_cyrillic_last  = models.CharField(
        "Last Name (Cyrillic Alphabet)" , max_length = 100, blank=True)
    name_cyrillic_first = models.CharField(
        "First Name (Cyrillic Alphabet)", max_length = 100, blank=True)
    nationality = models.CharField(max_length = 3, choices=LANGUAGES, blank=True)
    year_birth = models.IntegerField('Year of Birth', blank=True, null=True)
    year_death = models.IntegerField('Year of Death', blank=True, null=True)
    description = models.TextField(max_length = 1000, blank=True)

    def __str__(self):
        return self.get_name_latin()
    def get_absolute_url(self):
        return "/collection/creators/{}".format(self.slug)
    class Meta:
        ordering = ["name_latin_last", "name_latin_first"]
        unique_together = (
            ('name_latin_last', 'name_latin_first'),
            ('name_cyrillic_last', 'name_cyrillic_first')
        )

    def get_name_latin(self):
        output = ''
        if self.name_latin_last:
            output += self.name_latin_last
            if self.name_latin_first:
                output += ', '
        if self.name_latin_first:
            output += self.name_latin_first
        if output:
            return output
        else:
            return None

    def get_name_cyrillic(self):
        output = ''
        if self.name_cyrillic_last:
            output += self.name_cyrillic_last
            if self.name_cyrillic_first:
                output += ', '
        if self.name_cyrillic_first:
            output += self.name_cyrillic_first
        if output:
            return output
        else:
            return None

    def get_lifespan(self):
        if self.year_birth:
            if self.year_death:
                return str(self.year_birth) + "–" + str(self.year_death)
            else:
                return 'born ' + str(self.year_birth)
        elif self.year_death:
            return 'died ' + str(self.year_death)
        else:
            return 'dates unknown'
