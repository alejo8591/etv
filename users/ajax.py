# -*- coding: utf-8 -*-
from dajax.core import Dajax
from django.core.context_processors import csrf
from dajaxice.utils import deserialize_form
from dajaxice.decorators import dajaxice_register
from users.forms import RegistrationFormFranchisee
from users.classes.UserRegistration import UserRegistration

"""
    ajax working with two important files (classes):
    classes.UserRegistration: business logic queries and records as:
    - Shipping mail
    - Return information to the frontend

    forms.RegistrationFormFranchisee: form class parameters and form fields:
    - Query code franchisee
    - Availability franchisee
    - Email Verification
"""

@dajaxice_register(method='POST')
def send_form(request,form):
    dajax = Dajax()
    
    form = RegistrationFormFranchisee(deserialize_form(form))
    
    if request.method =='POST':
        
        if form.is_valid():
            # instantiating object UserRegistration
            formf = UserRegistration(form)
            # JSON for form data 
            data = formf.cleanData()
            # validation data: Franchisee code, email, Franchisee
            validFranchisee = formf.validDataFranchisee()
            print validFranchisee
            #checking fields not in use
            if (validFranchisee['franchisee'] == True and validFranchisee['email'] == True and validFranchisee['franchiseeCode']['flag'] == True and validFranchisee['franchiseeCode']['id'] >= 0 ):
                
                formf.saveUser(); formf.activationKey(); formf.newUserProfile()
                   
                 # change in the respective fields successful color
                for field in form.fields:
                    # removing the entry fields
                    dajax.remove('#id_%s' % field)
                    # adding fields not editable
                    dajax.append('#f_%s' % field, 'innerHTML','<span id="id_%s" class="input-medium uneditable-input">No puede Modificar</span>' % field)
                    dajax.remove_css_class('#label_%s' % field, 'label label-important')
                    dajax.add_css_class('#label_%s' % field, 'label label-success')
                    dajax.remove_css_class('#f_%s' % field, 'control-group error')
                    dajax.add_css_class('#f_%s' % field, 'control-group success')
                    dajax.remove('#label_%s' % field)
                    dajax.append('#f_%s'% field, 'innerHTML','<span id="label_%s" class="label label-success">Correcto</span>' % field)
                
                # Change other fields with successful Color
                dajax.remove_css_class('#errors','alert alert-info')
                dajax.remove_css_class('#errors','alert alert-error')
                dajax.add_css_class('#errors','alert alert-success')
                # adding button unmodifiable
                dajax.remove('#buttonSend')
                dajax.append('#my_form', 'innerHTML', '<a class="btn btn-primary disabled">Resgistrarme!</a>')
                dajax.add_css_class('#buttonSend', 'btn btn-primary disabled')
                
                dajax.assign('#errors', 'innerHTML', '<b>Muchas Gracias te Registraste con exito!</b>')
                
                message_correct = """
                                
                                  """
                dajax.assign('#modalBody', 'innerHTML', '<h5>Para tener en cuenta:</h5><span class="badge badge-inverse">1</span> Revisa tu correo electronico <span class="label label-info">%s</span>' % data['email'])
                # Modal with info subcriptor
                dajax.script("$('#myModal').modal('show')")
                # send email
                formf.send_mails('alejo8591@gmail.com')
                        
            # If the user or user code already exists or use   
            else:
                message_errors = """<h5><i class="icon-warning-sign"></i> Verificar los siguientes <span class="label label-important">ERRORES</span> en tu Registro como Franquiciado:</h5><br />
                                    <span class="badge badge-important">1</span> <b>La identificación o Documento ya existe</b><br />
                                    <span class="badge badge-important">2</span> <b>Cuenta de correo electrónico ya existe</b><br />
                                    <span class="badge badge-important">3</span> <b>Las contraseñas no concuerdan</b><br />
                                    <span class="badge badge-important">4</span> <b>El Código de referencia ya esta en uso</b><br />
                                    <span class="badge badge-important">5</span> <b>El Código de referencia indicado No existe</b>
                                     
                                 """
                dajax.assign('#modalBody', 'innerHTML', message_errors)
                dajax.script("$('#myModal').modal('show')")  
        else:
            dajax.remove_css_class('#errors','alert-info')
            dajax.add_css_class('#errors','alert alert-error')
            dajax.assign('#errors', 'innerHTML', 'Los Campos en color <b>Rojo</b> deben ser ingresados o Corregidos:')
            
            for error in form.errors:
                dajax.remove_css_class('#f_%s' % error, 'control-group success')
                dajax.add_css_class('#f_%s' % error, 'control-group error')
                dajax.remove('#label_%s'% error)
                dajax.append('#f_%s' % error, 'innerHTML', '<span id="label_%s" class="label label-important">Corregir este Campo</span>'% error)
        
        return dajax.json()
    
    else:
        return dajax.json()