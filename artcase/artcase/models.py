from django.db import models
from .constants import LANGUAGES, PUBLIC_CHOICES
import datetime
#from django_date_extensions.fields import ApproximateDateField


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

    creators = models.ManyToManyField('Creator', blank = True)
    media = models.ManyToManyField('Medium', blank = True)
    sizes = models.ManyToManyField('Size', blank = True)
    dates = models.ManyToManyField('Date', blank = True)
    values = models.ManyToManyField('Value', blank = True)

    #cultures = models.ManyToManyField('Culture', blank = True)
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
        max_length = 255, blank=True)
    description = models.TextField(max_length=100000, blank=True)

    edition_state = models.CharField(max_length=255, blank=True)
    edition_size  = models.IntegerField(blank=True, null=True)

    public = models.BooleanField(
        'Public or Private', choices=PUBLIC_CHOICES, default=False, blank=False)

    CONDITIONS = (
        ('poor', 'poor'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('very_good', 'very good'),
        ('excellent', 'excellent'),
        ('near_mint', 'near mint'),
        ('mint', 'mint'),
    )
    condition = models.CharField(
        max_length = 10, choices=CONDITIONS, blank=True)

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

class Medium(models.Model):
    def __str__(self):
        return self.get_display_name()
    class Meta:
        ordering = ["name"]
        verbose_name_plural = 'media'

    def get_display_name(self):
        d = dict(self.MEDIA)
        return d.get(self.name)

    #artifacts = models.ManyToManyField('Artifact',
    #    through=Artifact.media.through, blank = True)

    MEDIA = (
        ('acrylic', 'acrylic paint'),
        ('oil', 'oil paint'),
        ('ink', 'ink'),
        ('graphite', 'graphite'),
        ('mixed_media', 'mixed media'),
        ('aquatint', 'aquatint'),
        ('lithograph', 'lithograph'),
        ('etching', 'etching'),
        ('offset', 'offset'),
        ('lithograph_offset', 'lithograph/offset'),
    )
    name = models.CharField(max_length = 10,
        choices=MEDIA, blank=True, default="lithograph")

class Size(models.Model):
    def __str__(self):
        output = self.size_type + ': '
        if self.height:
            output += str(self.height)
            if self.width or self.depth:
                output += ' x '
        if self.width:
            output += str(self.width)
            if self.depth:
                output += ' x '
        if self.depth:
            output += str(self.depth)
        output += ' ' + self.unit
        return output
    TYPES = (
        ('object', 'object'),
        ('frame', 'frame'),
        ('mat', 'mat'),
        ('sheet', 'sheet'),
    )
    UNITS = (
        ('in', 'inches'),
        ('ft', 'feet'),
        ('mm', 'millimeters'),
        ('cm', 'centimeters'),
        ('m',  'meters'),
    )
    height = models.DecimalField(blank = True, null=True,
        max_digits=6, decimal_places=3)
    width = models.DecimalField(blank = True, null=True,
        max_digits=6, decimal_places=3)
    depth = models.DecimalField(blank = True, null=True,
        max_digits=6, decimal_places=3)
    size_type = models.CharField(max_length = 6, choices=TYPES,
        default = 'object', blank=False, null=False)
    unit = models.CharField(max_length = 2, choices=UNITS,
        default = 'in', blank=False, null=False)

class Date(models.Model):
    def __str__(self):
        if self.approx_year:
            return "{}: c.{}".format(self.qualifier, self.year)
        if self.approx_month:
            return "{}: {}".format(self.qualifier, self.year)
        if self.approx_day:
            return "{}: {} {}".format(self.qualifier, self.month_str, self.year)
        else:
            return "{}: {} {} {}".format(self.qualifier, self.day, self.month_str, self.year)

    class Meta:
        ordering = ["date"]

    @property
    def day(self):
        return(self.date.day)

    @property
    def month(self):
        return(self.date.month)

    @property
    def month_str(self):
        names = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        return(names[self.month - 1])

    @property
    def year(self):
        return(self.date.year)

    QUALIFIERS = (
        ('created', 'created'),
        ('started', 'started'),
        ('completed', 'completed'),
        ('printed', 'printed'),
        ('published', 'published'),
        ('restored', 'restored'),
    )

    date = models.DateField()
    # date can be approximate, e.g.:
        # date is unknown: Aug. 1945
        # just the year is known: 1945
        # even the year is approximate: c.1945
    # all parts of date (year, month, day) are required, however, by Django date fields; therefore, I'm marking which of this tuple is approximate, and deal with it after the fact.
    approx_day = models.BooleanField(default=False)
    approx_month = models.BooleanField(default=False)
    approx_year = models.BooleanField(default=False)

    qualifier = models.CharField(max_length=11, default='created',
        choices=QUALIFIERS, blank=True, null=True)
    location  = models.CharField(max_length=100, blank=True, null=True)

class Value(models.Model):
    def __str__(self):
        return "{0} {1} {2} {3}".format(self.value_type, self.date,
            self.value, self.agent)
    VALUE_TYPES = (
            ("fmv", "Fair Market"),
            ("rep", "Replacement"),
        )
    value_type = models.CharField(max_length = 3, blank=False, null=False,
        default="fmv", choices=VALUE_TYPES)
    date = models.DateField()
    value = models.DecimalField(blank = False, null=False,
        max_digits=10, decimal_places=2)
    agent = models.CharField(max_length = 100)