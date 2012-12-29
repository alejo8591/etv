from dajax.core import Dajax
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
            #checking fields not in use
            if (validFranchisee['franchisee'] == True and validFranchisee['email'] == True and validFranchisee['franchiseeCode']['flag'] == True):
                
                formf.saveUser(); formf.activationKey(); formf.newUserProfile()
                formf.send_mails('alejo8591@gmail.com')
                   
                 # change in the respective fields successful color
                for field in form.fields:
                    dajax.remove_css_class('#label_%s' % field, 'label label-important')
                    dajax.add_css_class('#label_%s' % field, 'label label-success')
                    dajax.remove_css_class('#f_%s' % field, 'control-group error')
                    dajax.add_css_class('#f_%s' % field, 'control-group success')
                    dajax.remove('#label_%s' % field)
                    dajax.append('#f_%s'% field, 'innerHTML','<span id="label_%s" class="label label-success">Correcto</span>'% field)
                
                dajax.remove_css_class('#errors','alert alert-info')
                dajax.remove_css_class('#errors','alert alert-error')
                dajax.add_css_class('#errors','alert alert-success')
                dajax.assign('#errors', 'innerHTML', '<b>Muchas Gracias se Registro con exito!</b>')
                dajax.assign('#modalBody', 'innerHTML', '<h5>Para tener en cuenta:</h5><span class="badge badge-inverse">1</span> Revisa tu correo electronico <span class="label label-info">%s</span>' % data['email'])
                # Announcement correct entry
                #dajax.script('$("#modal-body").append(function(){<h5>Para tener en cuenta:</h5><span class="badge badge-inverse">1</span> Revisa tu correo electronico <span class="label label-info">%s</span>});' % data['email'])
                #<span class="badge badge-inverse">2</span> Verifica el correo enviado por <span class="label label-info">alejo8591@gmail.com</span><span class="badge badge-inverse">3</span> por ultimo click en el enlace de <span class="label label-important">Finalizar Registro</span>
                dajax.script("$('#myModal').modal('show')")
                
            # If the user or user code already exists or use   
            else:
                dajax.assign('#modalBody', 'innerHTML', '<h5>Algo salio mal:</h5><span class="badge badge-inverse">1</span> Revisa tu correo electronico <span class="label label-info">%s</span>' % data['email'])
                # Announcement correct entry
                #dajax.script('$("#modal-body").append(function(){<h5>Para tener en cuenta:</h5><span class="badge badge-inverse">1</span> Revisa tu correo electronico <span class="label label-info">%s</span>});' % data['email'])
                #<span class="badge badge-inverse">2</span> Verifica el correo enviado por <span class="label label-info">alejo8591@gmail.com</span><span class="badge badge-inverse">3</span> por ultimo click en el enlace de <span class="label label-important">Finalizar Registro</span>
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