# -*- coding: utf-8 -*-
from django.db import models
import django.contrib.auth.models as djangoauth
from django.utils.translation import ugettext as _
from datetime import date, datetime
from django.db.models.signals import post_save

from datetime import datetime

class UserProfile(models.Model):
    CITY = (
        ('Bogotá','Bogotá'),
        ('Cali','Cali'),
        ('Barranquilla','Barranquilla'),
        ('Medellin','Medellin'),        
    )
    identification = models.OneToOneField(djangoauth.User)
    refFranchisee = models.ForeignKey('self', help_text="Usuario Franqiciado que lo referencia", verbose_name="Franquiciado Referenciado")
    firstName    = models.CharField(max_length=60, help_text="Ingrese su(s) Nombre(s)", verbose_name="Nombre(s)")
    lastName     = models.CharField(max_length=60, help_text="Ingrese su(s) Apellido(s)", verbose_name="Apellido(s)")
    disabled     = models.BooleanField(default=False)
    city         = models.CharField(max_length=60, choices= CITY, help_text="Ciudad donde vive", verbose_name="Ciudad")
    dateOfBirth  = models.DateField(help_text="Ciudad donde vive", verbose_name="Fecha de Nacimiento")
    phone        = models.CharField(max_length=60, help_text="Número de Telefono de contacto", verbose_name="Telefono")
    mobile       = models.CharField(max_length=60, help_text="Número de Telefono móvil de contacto", verbose_name="Telefono móvil")
    alternativePhone = models.CharField(max_length=60, help_text="Número de Telefono o FAX", verbose_name="Telefono/FAX")
    address      = models.CharField(max_length=60, help_text="Dirección de Residencia", verbose_name="Dirección")
    lastAccess   = models.DateTimeField(default=datetime.now, editable=False)
    #user activation through product registration
    activationKey= models.CharField(max_length=60, editable=False)
    keyExpires   = models.DateTimeField(editable=False)
    
    class Meta:
        ordering = ['firstName']
    
    def __unicode__(self):
            return self.firstName
        
def createUser(sender, instance, created, **kwargs):
        if created:
           profile = UserProfile()
           profile.userIDNumber = instance
           profile.save
            
post_save.connect(createUser, sender=djangoauth.User)

class CreateCodes(models.Model):
    franchisee  = models.ForeignKey('UserProfile', editable=False)
    code        = models.CharField(max_length=20, editable=False)
    UseFlagCode = models.BooleanField(editable=False)
    dateUseFlag = models.DateTimeField(editable=False)