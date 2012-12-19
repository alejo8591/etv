# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    # Fields for the creation of the user who is not registered
    identification = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario en el Sistema', 'class':'span3'}))
    email          = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'span3'}))
    passwordOne    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'contraseña base', 'class':'span3'}))
    passwordTwo    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Repetir contraseña base', 'class':'span3'}))
    franchiseeCode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Código Franquiciado', 'class':'span3'}))
    
    #Method for verifying that the user is not in the database
    def isValidFranchesee(franchisee):
        try:
            User.objects.get(username=franchisee)
        except User.DoesNotExist:
            return True
        return False
        
    # Method for creating the user in the database
    def save(self, new_data):
        u = User.objects.create_user(new_data['identification'],
                                    new_data['email'],
                                    new_data['password1'])
        u.is_active = False
        u.save()
        return u