# -*- coding: utf-8 -*-
from users.forms import RegistrationFormFranchisee
import datetime, random, sha
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage, EmailMultiAlternatives
from users.models import UserProfile, CreateCodes

class UserRegistration(object):
        
    def __init__(self, form):
        """
            Instantiating the `form` with ajax to process information
            :param form: Form object ajax.py
        """
        self._form = form
        
        
    def cleanData(self):
        """
            method or function responsible for cleaning objects oder
            `form` to be read by python, returns a JSON
        """
        # Clean Fields
        self._identification = self._form.cleaned_data['identification']
        self._email          = self._form.cleaned_data['email']
        self._passwordOne    = self._form.cleaned_data['passwordOne']
        self._passwordTwo    = self._form.cleaned_data['passwordTwo']
        self._franchiseeCode = self._form.cleaned_data['franchiseeCode']
        #JSON
        self._data = {
                'identification': self._identification,
                'email': self._email,
                'passwordOne':self._passwordOne,
                'passwordTwo':self._passwordTwo,
                'franchiseeCode':self._franchiseeCode 
            }
        
        return self._data
    
    
    def validDataFranchisee(self):
        """
            method or function which validates the following fields:
            :param franchisee: identification of the franchisee
            :param email: email the franchisee
            :param franchiseCode: franchisee referenced code that is available.
            
        """
        # verifying that the user does not exist
        self._validFranchisee = self._form.isValidFranchisee(self._identification)
        # verifying that the email does not exist
        self._validFranchiseeEmail = self._form.isValidFranchiseeEmail(self._email)
        # verifying that the user code does not exist or used
        self._validFranchiseeCode = self._form.isValidFranchiseeCode(self._franchiseeCode)
                
        return {'franchisee': self._validFranchisee, 'email': self._validFranchiseeEmail, 'franchiseeCode': self._validFranchiseeCode}
    
    
    def saveUser(self):
        """ Save the user """
        self._user = self._form.save(self._data)
        
    
    def activationKey(self):
        """
            This method or function is responsible for creating
            the activation code and expiration date
        """
        # Build the activation key for their account
        initial  = sha.new(str(random.random())).hexdigest()[:5]
        self._activationKey  = sha.new(initial+self._identification).hexdigest()
        self._keyExpires     = datetime.datetime.today() + datetime.timedelta(2)
        self._dataActivation = {'activatioCode':self._activationKey, 'keyExpires':self._keyExpires}
    
    
    def newUserProfile(self):
        """
            This method or function creates the new user along with the profile
            that is initially disabled, returns the number of the Franchisee
            which referenced where applicable.
        """
        # when the user registers with Code
        if self._validFranchiseeCode['flag'] == True and self._validFranchiseeCode['id'] >0:
            
            franchisee = UserProfile.objects.get(identification=self._validFranchiseeCode['id'])
            
            newProfile = UserProfile(
                        identification=self._user, activationKey=self._activationKey,
                        keyExpires=self._keyExpires, refFranchiseeCode=self._franchiseeCode,
                        refFranchisee=franchisee)
            #update Code in list for user; assigning values ​​necessary to use the code and date of use
            CreateCodes.objects.filter(code=self._data['franchiseeCode']).update(useFlagCode=True, dateUseFlag=datetime.datetime.now())
            
        # when the user is logged without Code
        else:
            newProfile = UserProfile(
                        identification=self._user, activationKey=self._activationKey,
                        keyExpires=self._keyExpires, refFranchiseeCode=None)
        
        # Save the profile
        newProfile.save()
        
        
    def send_mails(self, mail):
        """
            This method or function is responsible for sending the email
            to activate as the case of Franchisee or Franchisee Referenced  
        """
        subject = 'Confirmación de Registro en elevatusventas.com'
        # Send an email with the confirmation link
        if self._validFranchiseeCode['flag'] == True and self._validFranchiseeCode['id'] > 0:
             """
                To cut down on the repetitive nature of loading and rendering templates,
                Django provides a shortcut function which largely automates the process:
                render_to_string() in django.template.loader, which loads a template,
                renders it and returns the resulting string:
                
                In this case we use the template to use `email_franchisee_code.html`
                registered user Referenced Franchisee
                
             """
             # Data for Referenced Franchisee
             user = User.objects.get(id=self._validFranchiseeCode['id'])
        
             body = render_to_string('users/email_franchisee.html',{'activation_key': self._activationKey, 'identification': self._identification ,'first_name':user.first_name, 'last_name': user.last_name})
            
        elif self._validFranchiseeCode['flag'] == True and self._validFranchiseeCode['id'] == 0:
            body = "Hello, %s, and thanks for signing up for an \n elevatusventas.com account!\n\nTo activate your account, click this link within 48 \hours:\n\nhttp://127.0.0.1:8000/confirm/%s" % (
                        self._identification,
                        self._activationKey)
         
        message =  EmailMessage(subject, body, mail, [self._email])
        message.content_subtype = "html"  # Main content is now text/html
        message.send()