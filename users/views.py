from django.contrib.auth.forms import UserCreationForm

def new_user(request):
    if request.method=='POST':
        form = UserCreationForm(request.POST)
        if form.is_valid:
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = UserCreationForm()
    return render_to_response('./users/newuser.html', {'form':form}, context_instance=RequestContext(request))