from dajax.core import Dajax
from dajaxice.utils import deserialize_form
from dajaxice.decorators import dajaxice_register
from users.forms import RegistrationForm

@dajaxice_register(method='POST')
def send_form(request,form):
    dajax = Dajax()
    form = RegistrationForm(deserialize_form(form))
    if request.method=='POST':
        if form.is_valid():
            # 
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
            dajax.script("$('#myModal').modal({})")
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