import datetime, random, sha
from django import forms
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from users.models import UserProfile
from users.forms import RegistrationFormFranchisee, LoginForm
from django.template import RequestContext

def registerFranchisee(request):
    # enabled when not in production or not in the system
    
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('users/register_franchisee.html', {'has_account':True})
    
    form = RegistrationFormFranchisee()

    context = {'title':'register','legend':u'Registrate como Franquiciado!','form_register':form, 'has_account':False}
    # Return context with clean Form register, This solves the problem of csrf_token
    return render_to_response('users/register_franchisee.html', context, context_instance=RequestContext(request))
    
"""

"""
def confirmFranchisee(request, activation_key):

    if request.user.is_authenticated():
        return render_to_response('users/confirm.html', {'has_account': True})
    
    user_profile = get_object_or_404(UserProfile, activationKey=activation_key)
    print user_profile.keyExpires
    print datetime.datetime.today()
    
    if user_profile.keyExpires < datetime.datetime.today():
        return render_to_response('users/confirm.html', {'expired': True})
    
    user_account = user_profile.identification
    print user_account
    user_account.is_active = True
    user_account.save()
    return render_to_response('users/confirm.html', {'success': True})
"""
def loginUser(request):
    if request.user.is_authenticated():
        return render_to_response('users/confirm.html', {'has_account': True})
    login_form = LoginForm()
    print login_form
    context = {'login_form':login_form, 'has_account':False, 'register':'hola mundo'}
    return render_to_response('users/register_franchisee.html', context, context_instance=RequestContext(request))
"""