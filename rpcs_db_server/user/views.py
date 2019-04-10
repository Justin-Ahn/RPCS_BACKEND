from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.db.models import Q
from user.models import UserProfile, UserLocation, EmailRecord
from user.forms import UserRegisterForm, UserLoginForm, UserForgetPwdForm, UserResetPwdForm

from utils.sendEmail import sendEmail

# class CustomModelBackend(ModelBackend):
#     def authenticate(self, request, username=None, password=None):
#         print("Customize authenticate.")
#         try:
#             # user could login via either username or email
#             user = User.objects.get(Q(username=username) | Q(email=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None


# Create your views here.
# user login the website: url 'login'
def login_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'login.html', context)

    form = UserLoginForm(request.POST)
    context["loginForm"] = form

    # check login form validility
    if not form.is_valid():
        print("User Login Form is invalid ...")
        return render(request, 'login.html', context)

    username, password = form.cleaned_data["username"], form.cleaned_data["password"]
    print("{0}: {1}".format(username, password))
    user = authenticate(username=username, password=password)

    userProfile = UserProfile.objects.get(user=user)
    # check activation
    if not userProfile.activated:
        print("User has not been activated")
        context["msg"] = "User has not been activated."
        return render(request, 'login.html', context)
    # check login information
    if not user:
        print("User logged in failed.")
        context["msg"] = "username and password do not match or exist."
        return render(request, 'login.html', context)

    login(request, user)
    print("User logged in successfully.")
    return redirect('/')


# user log out the website: url 'logout'
@login_required
def logout_action(request):
    logout(request)
    print("User log out.")
    return redirect('/')
    

# user register the website: url 'register'
def register_action(request):
    context = {}
    if request.method == "GET":
        return render(request, 'register.html')

    form = UserRegisterForm(request.POST)
    context["registerForm"] = form
    if not form.is_valid():
        print("User Registration Form is invalid ...")
        return render(request, 'register.html', context)

    print("User Registration Form is valid.")
    username, email = form.cleaned_data['username'], form.cleaned_data['email']
    password = form.cleaned_data['password1']
    user = User.objects.create_user(username=username,
                                    email=email,
                                    password=password)
    user.save()
    profile = UserProfile(user=user, good=0, fair=0, bad=0)
    profile.save()
    sendEmail(email) # send registration email

    print("New user is created but not activated.")
    return redirect('/login')


# user edit the profile: url 'edit-profile'
@login_required
def edit_profile_action(request):
    context = {}
    user = request.user
    profile = UserProfile.objects.get(user=user)
    if request.method == "GET":
        context["user"] = user
        context["profile"] = profile
        return render(request, "edit-profile.html", context)

    
    profile.bio_text = request.POST.get("bio_text")
    profile.portrait = request.POST.get("portrait")
    profile.save()
    return redirect("/myprofile")


# user view profile: url 'myprofile'
@login_required
def view_profile_action(request):
    if request.method != "GET":
        raise Http404

    user = request.user
    profile = UserProfile.objects.get(user=user)
    context = {"user": user, "profile": profile}
    return render(request, "myprofile.html")


# user edit address: url 'edit-address'
@login_required
def edit_address_action(request):
    if request.method == "GET":
        return render(request, "edit-address.html")


# user view address: url 'my-address'
@login_required
def view_address_action(request):
    if request.method == "GET":
        return render(request, "myaddress.html")

def activate_action(request, code):
    emailRecords = EmailRecord.objects.filter(code=code)
    if len(emailRecords) == 1:
        emailRecord = emailRecords[0]
        email = emailRecord.email
        user = User.objects.get(email=email)
        userProfile = UserProfile.objects.get(user=user)
        userProfile.activated = True
        userProfile.save()
        print("A user clicked the activation link!")
        return render(request, 'login.html', {"msg": "User activate successfully!"})
    else:
        print("A user clicked the wrong reset-password link ...")
        return render(request, 'index.html')


# user could update password: url 'update-pwd'
def update_pwd_action(request):
    userResetPwdForm = UserResetPwdForm()
    if request.method == "GET":
        return render(request, 'reset-pwd.html', {'resetPwdForm': userResetPwdForm})

    context = {}
    form = UserResetPwdForm(request.POST)
    context["resetPwdForm"] = form

    if not form.is_valid():
        print("User update pwd form in invalid ...")
        return render(request, 'reset-pwd.html', context)

    newPwd = form.cleaned_data["password1"]
    username = form.cleaned_data["username"]
    user = User.objects.get(username=username)

    print("User: {0} update password.:{1}".format(user, newPwd))
    # update to new password
    user.set_password(newPwd)
    user.save()

    return render(request, 'login.html')


# user click reset password email link and get reset password page: url 'reset'
def get_reset_action(request, code):
    emailRecords = EmailRecord.objects.filter(code=code)
    if len(emailRecords) == 1:
        emailRecord = emailRecords[0]
        email = emailRecord.email
        print("A user clicked the reset-password link!")
        return render(request, 'reset-pwd.html')
    else:
        print("A user clicked the wrong reset-password link ...")
        return render(request, 'index.html')


# user click forget password link and get send reset password email page
# user click send email button and send reset password email: url 'forget'
def forget_pwd_action(request):
    userForgetPwdForm = UserForgetPwdForm()
    if request.method == "GET":
        return render(request, 'forgetpwd.html', {'forgetPwdForm': userForgetPwdForm})

    context = {}
    form = UserForgetPwdForm(request.POST)
    context["forgetPwdForm"] = form

    if not form.is_valid():
        print("User forget pwd form is invalid ...")
        return render(request, 'forgetpwd.html', context)

    email = form.cleaned_data['email']
    print("Send to %s"%(email))

    sendEmail(email, 'forget')
    return render(request, 'send-success.html')
