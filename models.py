
from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models



class Badge(models.Model):
    name = models.CharField(max_length=45)
    link = models.URLField(max_length=200, blank=True, null=True)
    imageURL = models.URLField(max_length=200)
    
    
    def __unicode__(self):
        return u'%s' % (self.name)
    
    class Meta:
        ordering = ['name']
        
        
        

class BadgeUser(models.Model):
    google_id = models.CharField(max_length=65, verbose_name='Google ID', blank=True, null=True)
    user = models.ForeignKey(User, blank=True, null=True)
    badges = models.ManyToManyField(Badge, blank=True, null=True)
    
    
    
    
    
admin.site.register(Badge)
admin.site.register(BadgeUser)
        