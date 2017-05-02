from django.shortcuts import redirect

def edit_user(request):
    name=request.user.username
    return redirect('/' + name + '/update')

def profile(request):
    name=request.user.username
    return redirect('/' + name + '/profile')