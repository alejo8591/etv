# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.contrib.auth.models import User
from users.models import CreateCodes, UserProfile

class RegistrationFormFranchisee(forms.Form):
    # Fields for the creation of the user who is not registered
    identification = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario en el Sistema', 'class':'span3'}))
    email          = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'span3'}))
    passwordOne    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Escriba la Contraseña', 'class':'span3'}))
    passwordTwo    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Repita la Contraseña', 'class':'span3'}))
    franchiseeCode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Código Franquiciado', 'class':'span3'}), required=False, initial=None)
    
    # Method for verifying that the user and data is not in the database
    def isValidFranchisee(self, franchisee):
        try:
            User.objects.get(username=franchisee)
        except User.DoesNotExist:
            return True
        return False
    
    def isValidFranchiseeEmail(self, email):
        try:
            User.objects.get(email=email)
        except User.DoesNotExist:
            return True
        return False
    
    def isValidFranchiseeCode(self, franchiseeCode):
        try:
            franchiseeReg = CreateCodes.objects.get(code=franchiseeCode) 
        except CreateCodes.DoesNotExist:
            # checking if the field is blank franchiseeCode or invalid 
            if franchiseeCode == '':
                return {'message':u'No suministra código de referencia para Franquiciado', 'flag':False, 'id':0}
            #invalid FranchiseeCode
            return {'message':u'Este código No existe', 'flag':None, 'id':None}
        # if users code is used or not
        if franchiseeReg.useFlagCode == True:
            return {'message':u'Este código ya esta en Uso', 'flag':False, 'id':-1}
        else:
            return {'message': u'La cedula del franquiciado que te referencia es %s' % (str(franchiseeReg.franchisee.identification.username)), 'flag': True, 'id': franchiseeReg.franchisee.identification.id}
    
    # Method for creating the user in the database
    def save(self, data):
        u = User.objects.create_user(data['identification'],
                                    data['email'],
                                    data['passwordOne'])
        u.is_active = False
        u.save()
        return u