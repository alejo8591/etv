import datetime, random, sha
from django import forms
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from users.models import UserProfile
from users.forms import RegistrationFormFranchisee
from dajaxice.core import dajaxice_functions

def registerFranchisee(request):
    # enabled when not in production or not in the system
    """
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('users/register.html', {'has_account':True})
    """
    form = RegistrationFormFranchisee()
    
    context = Context({'title':'register','legend':'Registrate como Franquiciado!','form':form})
    # Return context with clean Form register
    return render_to_response('users/register_franchisee.html', context)
    
"""

"""
def confirmFranchisee(request, activation_key):
    if request.user.is_authenticated():
        return render_to_response('users/confirm.html', {'has_account': True})
    
    user_profile = get_object_or_404(UserProfile,
                                     activation_key=activation_key)
    
    if user_profile.key_expires < datetime.datetime.today():
        return render_to_response('users/confirm.html', {'expired': True})
    
    user_account = user_profile.user
    user_account.is_active = True
    user_account.save()
    return render_to_response('confirm.html', {'success': True})