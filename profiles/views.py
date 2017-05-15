from django.shortcuts import redirect

def edit_user(request):
    name=request.user.username
    #nameid=str(request.user.id)
    return redirect('/profile/' + name + '/update')

#if user wants to see a profile
def profile(request):
    name=request.user.username
    #nameid = str(request.user.id)
    return redirect('/profile/' + name + '/')

def favorites(request):
    name=request.user.username
    #nameid = str(request.user.id)
    return redirect('/profile/' + name + '/favs')

#if just loggen in
