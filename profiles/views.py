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


def add_recipe(request):
    name=request.user.username
    return redirect('/profile/' + name + '/post')

def my_recipes(request):
    name=request.user.username
    return redirect('/profile/' + name + '/recipes')

#if just loggen in
