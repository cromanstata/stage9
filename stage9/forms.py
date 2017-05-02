from allauth.account.forms import LoginForm, SignupForm

#pushcheck1

class MyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['remember'].label = 'Stay signed in'
        self.fields['remember'].initial = True
