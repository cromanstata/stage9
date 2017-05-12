from django.shortcuts import redirect

def edit_user(request):
    name=request.user.username
    #nameid=str(request.user.id)
    print("edit user in profiles.views.edit_user access")
    print(name)
    return redirect('/profile/' + name + '/update')

#if user wants to see a profile
def profile(request):
    name=request.user.username
    #nameid = str(request.user.id)
    print("edit user in profiles.views.edit_user access")
    print(name)
    return redirect('/profile/' + name + '/')

#if just loggen in
