# -*- coding: utf-8 -*-
from django.db import models, connection
from django.db.models.sql import InsertQuery
from django.contrib.auth.models import User
from django.utils.translation import ugettext as _
from datetime import date, datetime
from django.db.models.signals import post_save
from users.classes.UsersCodes import UserCode
from users.classes.BulkInsert import Bulk
from django.conf import settings

from datetime import datetime

class UserProfile(models.Model):
    """
        It extends the model model user base that comes with django and gives
        the performance needed for working with user data
    """
    CITY = (
        (u'Bogotá',u'Bogotá'),
        (u'Cali',u'Cali'),
        (u'Barranquilla',u'Barranquilla'),
        (u'Medellin',u'Medellin'),        
    )
    identification = models.OneToOneField(User, primary_key=True)
    refFranchisee  = models.ForeignKey('self', help_text="Usuario Franqiciado que lo referencia", verbose_name="Franquiciado Referenciado", blank=True, null=True)
    city           = models.CharField(max_length=60, choices= CITY, help_text="Ciudad donde vive", verbose_name="Ciudad", blank=True, null=True)
    dateOfBirth    = models.DateField(help_text="Fecha de Nacimiento", verbose_name="Indique la Fecha de Nacimiento", blank=True, null=True)
    photo          = models.ImageField(help_text="Foto del Usuario", verbose_name="Foto", blank=True, null=True, upload_to="uploads")
    phone          = models.CharField(max_length=60, help_text="Número de Telefono de contacto", verbose_name="Telefono", blank=True, null=True)
    mobile         = models.CharField(max_length=60, help_text="Número de Telefono móvil de contacto", verbose_name="Telefono móvil", blank=True, null=True)
    alternativePhone = models.CharField(max_length=60, help_text="Número de Telefono o FAX", verbose_name="Telefono/FAX", blank=True, null=True)
    address        = models.CharField(max_length=60, help_text="Dirección de Residencia", verbose_name="Dirección", blank=True, null=True)
    lastAccess     = models.DateTimeField(auto_now=True, editable=False)
    #user activation through product registration
    activationKey  = models.CharField(max_length=60, editable=False, blank=True, null=True)
    keyExpires     = models.DateTimeField(editable=False, blank=True, null=True)
    refFranchiseeCode = models.CharField(max_length=20, editable=False, blank=True, null=True, unique=True)
    
    class Meta:
        ordering = ['identification']
    
    def __unicode__(self):
            return "%s" %(self.identification) 

def createUser(sender, instance, created, **kwargs):
        if created:
           profile = UserProfile()
           profile.identification = instance
           profile.save
            
post_save.connect(createUser, sender=User)

class CreateCodes(models.Model):
    """
        This model is based on the class 'BulkInsert' to create the 20 codes that are
        assigned to the franchisee or franchisee referenced and anchor with
        your franchisee level
    
    """
    franchisee  = models.ForeignKey('UserProfile', to_field='identification')
    code        = models.CharField(max_length=20, editable=False, unique=True)
    useFlagCode = models.BooleanField(default=False, editable=False)
    dateUseFlag = models.DateTimeField(editable=False, blank=True, null=True)
    dateCreateCode = models.DateTimeField(auto_now_add=True, editable=False)
    
    def __unicode__(self):
        return "%s %s"%(self.franchisee, self.code)
    
    # saving codes generated for franchisees 
    def save(self):
        """
            is sent to the class UserCode parameter of 20 and 8 for the number
            of codes and code length.
        """
        bulk = Bulk(); values = []; self.cod = UserCode(20,8)
        self.codes = self.cod.generateCodes()
        for i in range(len(self.codes)):values.append(CreateCodes(franchisee = self.franchisee, code = self.codes[i], useFlagCode = False, dateUseFlag = None, dateCreateCode = datetime.now()))
        bulk.insertMany(CreateCodes,values)