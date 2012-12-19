import datetime, random, sha
from django import forms
from django.template import Context
from django.shortcuts import render_to_response, get_object_or_404
from django.core.mail import send_mail

from users.models import UserProfile
from users.forms import RegistrationForm
from dajaxice.core import dajaxice_functions

def register(request):
    # enabled when not in production or not in the system
    """
    if request.user.is_authenticated():
        # They already have an account; don't let them register again
        return render_to_response('users/register.html', {'has_account':True})
    """
    form = RegistrationForm()
    context = Context({'title':'register','legend':'Register New Users','form':form})
    """
    if request.POST:
        new_data = request.POST.copy()
        errors = manipulator.get_validation_errors(new_data)
        if not errors:
            # Save ther user
            manipulator.do_html2python(new_data)
            new_user = manipulator.save(new_data)
            
            # Build the activation key for their account
            salt = sha.new(str(random.random())).hexdigest()[:5]
            activation_hey = sha.new(salt+new_user.username).hexdigest()
            key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # Create and save their profile
            new_profile = UserProfile(
                userIDNumber=new_user, activationKey=activation_key,
                keyExpires=key_expires)
            new_profile.save()
            
            # Send an email with the confirmation link                                                                                                                      
            email_subject = 'Your new example.com account confirmation'
            email_body = "Hello, %s, and thanks for signing up for an \example.com account!\n\nTo activate your account, click this link within 48 \hours:\n\nhttp://example.com/accounts/confirm/%s" % (
                            new_user.username,
                            new_profile.activation_key)
            send_mail(email_subject,
                      email_body,
                      'accounts@example.com',
                      [new_user.email])
            
            return render_to_response('users/register.html', {'created': True})
        else:
            errors = new_data = {}
     """
     
    if request.method == 'POST':
        # A form bound to the POST data
        form =  RegistrationForm(request.POST)
        if form.is_valid():
            # Clean Fields
            identification =form.cleaned_data['identification']
            email          =form.cleaned_data['email']
            passwordOne    =form.cleaned_data['passwordOne']
            passwordTwo    = form.cleaned_data['passwordTwo']
            franchiseeCode = form.cleaned_data['franchiseeCode']
            # JSON Fields 
            data = {
                'identification': identification,
                'email': email,
                'passwordOne':passwordOne,
                'passwordTwo':passwordTwo,
                'franchiseeCode':franchiseeCode 
            }
            
            # verifying that the user does not exist
            validFranchesee = form.isValidFranchesee(data['identification'])
            if validFranchesee:
                
                # Build the activation key for their account
                salt = sha.new(str(random.random())).hexdigest()[:5]
                activation_hey = sha.new(salt+new_user.username).hexdigest()
                key_expires = datetime.datetime.today() + datetime.timedelta(2)
            
            # If the user already exists then announces that already exists    
            else:
                
                return 
            
            return HttpResponseRedirect('/thanks/')
        else:
            context = Context({'title':'register','legend':'Register New Users','form':form})
    # Return context with clean Form register
    return render_to_response('users/register.html', context)
    
    
def confirm(request, activation_key):
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