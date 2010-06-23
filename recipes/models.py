from django.db import models
from tagging.fields import TagField
from django.utils.translation import ugettext_lazy as _
from datetime import datetime
from markitup.fields import MarkupField

class StandardMetadata(models.Model):
    """
    A basic (abstract) model for metadata.
    
	Subclass new models from 'StandardMetadata' instead of 'models.Model'.
    """
    created = models.DateTimeField(default=datetime.now, editable=False)
    updated = models.DateTimeField(default=datetime.now, editable=False)
    
    class Meta:
        abstract = True
    
    def save(self, *args, **kwargs):
        self.updated = datetime.now()
        super(StandardMetadata, self).save(*args, **kwargs)

class ApprovedManager(models.Manager):
    def get_query_set(self):
        return super(ApprovedManager, self).get_query_set().filter(approved=True)

class Recipe(StandardMetadata):
    title = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)
    description = models.TextField(_('description'), blank=True, null=True)
    ingredients = models.TextField(_('ingredients'), blank=True, null=True)
    directions = models.TextField(_('directions'))
    author = models.CharField(max_length=50, blank=True, null=True)
    email = models.EmailField(_('email'), blank=True, null=True)
    approved = models.BooleanField(_('approved'))
    tags = TagField()
    
    objects=models.Manager()
    approved_objects=ApprovedManager()
    
    def __unicode__(self):
        return self.title
    
    class Meta:
        
        ordering = ['title']
    
    @models.permalink
    def get_absolute_url(self):
        return ('recipes-detail', [self.slug])
