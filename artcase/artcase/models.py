from django.db import models
from taggit.managers import TaggableManager
from .fields import WhereWhenField
from django.utils.timezone import now

class Base(models.Model)
    class Meta:
        abstract = True
    created = models.DateTimeField(default=now())
    modified = models.DateTimeField(auto_now=True)

class Work(Base):
    title = models.CharField(max_length=100)
    sku = models.CharField(max_length=100)

    # created = WhereWhenField(max_length=100)

    UNITS = (
        ('cm', 'centimeters'),
        ('in', 'inches'),
    )
    size_h = models.DecimalField(max_digits=6, decimal_places=3)
    size_w = models.DecimalField(max_digits=6, decimal_places=3)
    size_d = models.DecimalField(max_digits=6, decimal_places=3)
    size_unit = models.CharField(max_length=2, choices=UNITS)

    CONDITIONS = (
        ('loss', 'total loss'),
        ('poor', 'poor'),
        ('fair', 'fair'),
        ('good', 'good'),
        ('very_good', 'very good'),
        ('excellent', 'excellent'),
        )
    condition = models.CharField(max_length=10, choices=CONDITIONS)

    STATUSES = (
        ('?', 'missing'),
        ('display', 'on display'),
        ('storage', 'in storage'),
        )
    status = models.CharField(max_length=10, choices=STATUSES)
    notes = models.TextField()

    subjects = TaggableManager()

    location = models.ForeignKey('location')
    medium = models.ForeignKey('medium')

    creators = models.ManyToManyField('creator')
    values = models.ManyToManyField('value')
    categories = models.ManyToManyField('category')
    images = models.ManyToManyField('image')

    collections = models.ManyToManyField('collection')
    exhibits = models.ManyToManyField('exhibit')


class Creator(Base):
    name_first = models.CharField(max_length=50)
    name_last = models.CharField(max_length=50)

    #born = WhereWhenField(max_length=100)
    #died = WhereWhenField(max_length=100)


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
    value = models.DecimalField(max_digits=12, decimal_places=2)
    value_currency = models.CharField(
        max_length=3,
        choices=CURRENCIES,
        default='usd',
        )
    value_type = models.CharField(
        max_length=3,
        choices=TYPES,
        default='fmv',
        )

    date = models.DateField(default=now())


class Location(Base):
    name = models.CharField(max_length=100)
    address = models.TextField()
    sublocation = models.TextField()


class Medium(Base):
    name = models.CharField(max_length=100)


class Image(Base):
    image = models.ImageField(
        height_field='image_h',
        width_field='image_w',
        )
    image_h = models.IntegerField()
    image_w = models.IntegerField()

    ASPECTS = (
        ('recto','recto'),
        ('verso','verso'),
        ('detail','detail'),
        ('signature','signature'),
        )
    aspect = models.CharField(max_length=10, choices=ASPECTS)
    caption = models.TextField()


class Category(Base):
    '''
    Hierarchical organization, particular to collection
    '''
    name = models.CharField(max_length=100)
    description = models.TextField()
    parent = models.ForeignKey('self', on_delete=models.CASCADE)
    

class Collection(Base):
    name = models.CharField(max_length=100)
    description = models.TextField()


class Exhibit(Base):
    name = models.CharField(max_length=100)
    description = models.TextField()