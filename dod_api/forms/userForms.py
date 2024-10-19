from django import forms

# Registration Form
class RegisterForm(forms.Form):
    firstname = forms.CharField(max_length=100, label="First Name", widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'Enter your first name'}))
    lastname = forms.CharField(max_length=100, label="Last Name", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your last name'}))
    email = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email here'}))
    phone = forms.CharField(max_length=10, label="Mobile Number", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your mobile number '}))

# OTP Verification Form for Registration
class BaseOtpForm(forms.Form):
    otp = forms.CharField(max_length=6, label="Enter OTP", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your OTP here' }))

# Login Form (Phone Number)
class LoginForm(forms.Form):
    phone = forms.CharField(max_length=13, label="Mobile Number", widget=forms.TextInput(
        attrs={'class': 'form-control','placeholder': 'Enter your mobile number' }))


