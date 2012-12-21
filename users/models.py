# -*- coding: utf-8 -*-
from django.db import models
import django.contrib.auth.models as djangoauth
from django.utils.translation import ugettext as _
from datetime import date, datetime
from django.db.models.signals import post_save
from users.classes.UsersCodes import UserCode

from datetime import datetime

class UserProfile(models.Model):
    CITY = (
        ('Bogotá','Bogotá'),
        ('Cali','Cali'),
        ('Barranquilla','Barranquilla'),
        ('Medellin','Medellin'),        
    )
    identification = models.OneToOneField(djangoauth.User)
    refFranchisee  = models.ForeignKey('self', help_text="Usuario Franqiciado que lo referencia", verbose_name="Franquiciado Referenciado", blank=True, null=True)
    firstName      = models.CharField(max_length=60, help_text="Ingrese su(s) Nombre(s)", verbose_name="Nombre(s)")
    lastName       = models.CharField(max_length=60, help_text="Ingrese su(s) Apellido(s)", verbose_name="Apellido(s)")
    disabled       = models.BooleanField(default=False)
    city           = models.CharField(max_length=60, choices= CITY, help_text="Ciudad donde vive", verbose_name="Ciudad")
    dateOfBirth    = models.DateField(help_text="Ciudad donde vive", verbose_name="Fecha de Nacimiento")
    phone          = models.CharField(max_length=60, help_text="Número de Telefono de contacto", verbose_name="Telefono", blank=True, null=True)
    mobile         = models.CharField(max_length=60, help_text="Número de Telefono móvil de contacto", verbose_name="Telefono móvil")
    alternativePhone = models.CharField(max_length=60, help_text="Número de Telefono o FAX", verbose_name="Telefono/FAX", blank=True, null=True)
    address        = models.CharField(max_length=60, help_text="Dirección de Residencia", verbose_name="Dirección")
    lastAccess     = models.DateTimeField(auto_now=True, editable=False)
    #user activation through product registration
    activationKey  = models.CharField(max_length=60, editable=False, blank=True, null=True)
    keyExpires     = models.DateTimeField(editable=False, blank=True, null=True)
    
    class Meta:
        ordering = ['firstName']
    
    def __unicode__(self):
            return "%s %s %s" %(self.firstName, self.lastName, self.identification)
    # Saving franchisee regarding whether or not referenced
    def save(self, *args, **kwargs):
        r = UserProfile.objects.all()
        if(len(r)==0): id=1
        super(UserProfile, self).save(*args, **kwargs)
        
def createUser(sender, instance, created, **kwargs):
        if created:
           profile = UserProfile()
           profile.identification = instance
           profile.save
            
post_save.connect(createUser, sender=djangoauth.User)

class CreateCodes(models.Model):
    franchisee  = models.ForeignKey('UserProfile')
    code        = models.CharField(max_length=20, editable=False)
    UseFlagCode = models.BooleanField(default=False, editable=False)
    dateUseFlag = models.DateTimeField(editable=False, blank=True, null=True)
    dateCreateCode = models.DateTimeField(auto_now_add=True, editable=False)
    
    def createCodes(self):
        self.cod = UserCode()
        self.codes = self.cod.generateCodes(str(self.franchisee))
        for i in range(len(self.codes)):
            self.franchisee = self.franchisee
            self.code = self.codes[i]
            self.UseFlagCode = False
            self.dateUseFlag = None
            self.dateCreateCode = datetime.now()
            super(CreateCodes, self).save(*args, **kwargs)
    
    def save(self, *args, **kwargs):
        super(CreateCodes, self).save(*args, **kwargs)