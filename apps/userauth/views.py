from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('/')
    else:
        pass

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                return(HttpResponse("Your Account is disabled"))
        else:
            return render(request, "userauth/login.html", {'invalid': True })

    else:
        return render(request, 'userauth/login.html', {})

@login_required
def user_logout(request):
	logout(request)
	return HttpResponseRedirect('/')