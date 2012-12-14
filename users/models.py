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
    userIDNumber = models.OneToOneField(djangoauth.User)
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

# Model building codes to be used by franchisee 
class UserFranchiseeCode(models.Model):
    # partnership with the franchisee or franchisee referenced
    userFranchisee           = models.ForeignKey(UserProfile, help_text="Códigos del Franquiciado")
    # code is 4 initially four numbers for users franchisees referenced
    userFranchiseeCode       = models.CharField(max_length=20);
    # flag of the use code: True = code used and False = Not used
    userFranchiseeCodeFlag   = models.BooleanField(default=False, editable=False)
    # Creation Date
    userFranchiseeDateCreate = models.DateTimeField(default=datetime.now, editable=False)
    # Use the code date
    userFranchiseeDateUse    = models.DateTimeField(editable=False)