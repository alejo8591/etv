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
            dajax.remove_css_class('#my_form input', 'error')
            dajax.alert("Form is_valid(), your username is: %s" % form.cleaned_data.get('identification'))
        else:
            dajax.remove_css_class('#my_form input', 'error')
            for error in form.errors:
                dajax.add_css_class('#id_%s' % error, 'inputError')
    
        return dajax.json()
    else:
        return dajax.json()