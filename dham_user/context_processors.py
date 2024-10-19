# your_app/context_processors.py

from dod_api.forms.userForms import RegisterForm, LoginForm, BaseOtpForm

def forms_in_header(request):
    return {
        'register_form': RegisterForm(),
        'login_form': LoginForm(),
        'otp_form': BaseOtpForm(),
    }
