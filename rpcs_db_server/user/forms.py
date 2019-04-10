from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django import forms

# check pwd and confrim_pwd are valid
def checkPwd(cleaned_data):
    pw1 = cleaned_data.get('password1')
    pw2 = cleaned_data.get('password2')
    print("password1: %s\npassword2: %s"%(pw1, pw2))
    if pw1 and pw2 and pw1 != pw2:
        raise forms.ValidationError("Passwords did not match.")

################################################################################

class UserRegisterForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    password1 = forms.CharField(min_length=8, required=True)
    password2 = forms.CharField(min_length=8, required=True)

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        checkPwd(cleaned_data)
        return cleaned_data

    def clean_username(self):
        print("username cleaning ...")
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__exact=username):
            raise forms.ValidationError("Username already exists.")
        print("username does not exist")
        return username

    def clean_email(self):
        print("email cleaning ...")
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__exact=email):
            raise forms.ValidationError("Email already exists.")
        print("email does not exist")
        return email


class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=200, required=True)
    password = forms.CharField(required=True)


class UserForgetPwdForm(forms.Form):
    email = forms.EmailField(required=True)


class UserResetPwdForm(forms.Form):
    password1 = forms.CharField(required=True, min_length=8)
    password2 = forms.CharField(required=True, min_length=8)
    username = forms.CharField(required=True)

    def clean(self):
        cleaned_data = super(UserResetPwdForm, self).clean()
        checkPwd(cleaned_data)
        return cleaned_data    
