# -*- coding: utf-8 -*-
from tastypie import fields
from tastypie.resources import ModelResource
from users.models import UserProfile
from django.contrib.auth.models import User
from tastypie.serializers import Serializer


class UserResource(ModelResource):
    class Meta:
        queryset = User.objects.all()
        resource_name = 'user'
        excludes = ['email', 'password', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'id']
        serializer = Serializer(formats=['json'])
        
class UserProfileResource(ModelResource):
    profiles = fields.OneToOneField(UserResource, 'identification')
    
    class Meta:
        queryset = UserProfile.objects.all()
        resource_name = 'profile'
        serializer = Serializer(formats=['json'])