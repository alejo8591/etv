# -*- coding: utf-8 -*-
from django import forms
from django.core import validators
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    
    identification = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Usuario en el Sistema', 'class':'span3'}))
    email          = forms.EmailField(widget=forms.TextInput(attrs={'placeholder':'email', 'class':'span3'}))
    passwordOne    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'contraseña base', 'class':'span3'}))
    passwordTwo    = forms.CharField(widget=forms.PasswordInput(render_value=False, attrs={'placeholder':'Repetir contraseña base', 'class':'span3'}))
    franchiseeCode = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Código Franquiciado', 'class':'span3'}))
"""       
        def isValidUsername(self, field_data,all_data):
            try:
                User.objects.get(username=field_data)
            except User.DoesNotExist:
                return    
            raise validators.ValidationError("The Username '%s' is alredy taken.") %(field_data)
        
        def save(self, new_data):
            u = User.objects.create_user(new_data['username'],
                                        new_data['email'],
                                        new_data['password1'])
            u.is_active = False
            u.save()
            return u
"""