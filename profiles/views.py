from django.shortcuts import redirect

def edit_user(request):
    name=request.user.username
    nameid=str(request.user.id)
    return redirect('/profile/' + name + '/' + nameid + '/update')

def profile(request):
    name=request.user.username
    nameid = str(request.user.id)
    return redirect('/profile/' + name + '/' + nameid + '/')
