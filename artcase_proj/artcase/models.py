from .fields import WhereWhenField
from django.db import models
from django.urls import reverse
from django.utils.timezone import now
from taggit.managers import TaggableManager
from django.contrib.auth.models import User


class Base(models.Model):
    class Meta:
        abstract = True
    created = models.DateTimeField(default=now)
    modified = models.DateTimeField(auto_now=True)


class Work(Base):
    class Meta:
        unique_together = ('sku', 'owner')

    title = models.CharField(
        max_length=100,
        blank=False,
        )
    sku = models.SlugField(
        max_length=100,
        blank=False,
        )
    owner = models.ForeignKey(User, default=1)

    # created = WhereWhenField(max_length=100)

    UNITS = (
        ('cm', 'centimeters'),
        ('in', 'inches'),
    )
    size_h = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        )
    size_w = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        )
    size_d = models.DecimalField(
        max_digits=6,
        decimal_places=3,
        blank=True,
        null=True,
        )
    size_unit = models.CharField(
        max_length=2,
        choices=UNITS,
        default='in',
        blank=False,
        )

    CONDITIONS = (
        ('loss', 'total loss'),
        ('poor', 'poor'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('vgood', 'very good'),
        ('excel', 'excellent'),
        )
    condition = models.CharField(
        max_length=5,
        choices=CONDITIONS,
        blank=True,
        )

    STATUSES = (
        ('?', 'missing'),
        ('display', 'on display'),
        ('storage', 'in storage'),
        )
    status = models.CharField(
        max_length=10,
        choices=STATUSES,
        blank=True,
        )
    notes = models.TextField(
        blank=True,
        )

    subjects = TaggableManager(blank=True)

    location = models.ForeignKey(
        'location',
        blank=True,
        null=True,
        )
    medium = models.ForeignKey(
        'medium',
        blank=True,
        null=True,
        )
    creators = models.ManyToManyField(
        'creator',
        blank=True,
        )
    values = models.ManyToManyField(
        'value',
        blank=True,
        )
    categories = models.ManyToManyField(
        'category',
        blank=True,
        )
    images = models.ManyToManyField(
        'image',
        blank=True,
        )
    collections = models.ManyToManyField(
        'collection',
        blank=True,
        )

    def get_absolute_url(self):
        return reverse('artcase:work_detail', args=[self.sku])

    def __str__(self):
        return self.title


class Creator(Base):
    first_name = models.CharField(
        max_length=50,
        blank=True,
        )
    last_name = models.CharField(
        max_length=50,
        blank=False,
        )

    #born = WhereWhenField(max_length=100, blank=True,)
    #died = WhereWhenField(max_length=100, blank=True,)


class Value(Base):
    CURRENCIES = (
        ('usd', 'US Dollar'),
        ('eur', 'Euro'),
        ('gbp', 'British Pound'),
    )
    TYPES = (
        ('fmv', 'fair market value'),
        ('rpv', 'replacement value'),
    )
    value = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=False,
        )
    value_currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default='usd',
        blank=False,
        )
    value_type = models.CharField(
        max_length=3,
        choices=TYPES,
        default='fmv',
        blank=False,
        )

    date = models.DateField(
        default=now,
        blank=True,
        )


class Location(Base):
    name = models.CharField(
        max_length=100,
        blank=False,
        )
    address = models.TextField(
        blank=True,
        )
    sublocation = models.TextField(
        blank=True,
        )


class Medium(Base):
    class Meta:
        verbose_name_plural = "media"
    name = models.CharField(
        max_length=100,
        blank=False,
        )


class Image(Base):
    image = models.ImageField(
        height_field='image_h',
        width_field='image_w',
        blank=False,
        )
    image_h = models.IntegerField()
    image_w = models.IntegerField()

    ASPECTS = (
        ('recto','recto'),
        ('verso','verso'),
        ('detail','detail'),
        ('signature','signature'),
        )
    aspect = models.CharField(
        max_length=10,
        choices=ASPECTS,
        blank=True,
        )
    caption = models.TextField(
        blank=True,
        )


class Category(Base):
    class Meta:
        verbose_name_plural = "categories"
    '''
    Hierarchical organization, particular to collection
    '''
    name = models.CharField(
        max_length=100,
        blank=False,
        )
    description = models.TextField(
        blank=True,
        )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        )


class Collection(Base):
    name = models.CharField(
        max_length=100,
        blank=False,
        )
    description = models.TextField(
        blank=True,
        )