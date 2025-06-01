from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import get_user_model, authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from lab_project.settings import EMAIL_HOST_USER

from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm

User = get_user_model()

# Create your views here.
def signup(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        mobile_no = request.POST['mobile_no']
        username = request.POST['username']
        password = request.POST['password']
        confirmpassword = request.POST['confirmpassword']

        if password == confirmpassword:
            if User.objects.filter(username = username).exists():
                messages.info(request, "Username is already taken.")
                return redirect('signup')
            if User.objects.filter(email = email).exists():
                messages.info(request, "Email is already taken.")
                return redirect('signup')
            else:
                verf_link = str(uuid.uuid4())
                user = User.objects.create_user(first_name = first_name, last_name = last_name, email = email, username = username, mobile_no = mobile_no, password = password, verf_link = verf_link)
                user.save()

                send_email(email, verf_link)
                
                return redirect('verify_account')
        else:
            messages.info(request, "Passwords do not match.")
            return redirect('signup')
        
    else:
        return render(request, "signup.html")

def user_login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email = email, password = password)

        if user is not None:
            if user.email_verified == False:
                if not user.is_superuser:
                    messages.info(request, "Your email is not verified. Please verify your email before logging in")
                    
                    return redirect("login")
            
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, "Invalid email and password")
            return redirect("login")
    else:
        return render(request, "login.html")

def user_logout(request):
    logout(request)
    return redirect("/")

def link_send(request):
    return render(request, 'verify_account.html')

def send_email(email, link):
    sub = "Please Verify | CSE471 Lab Project Summer 2024"
    msg = f"Please click on the link to verify your account http://127.0.0.1:8000/account/verify/{link}"
    email_from = settings.EMAIL_HOST_USER
    email_to = [email]
    send_mail(sub, msg, email_from, email_to)

def verify(request, verf_link):
    user = User.objects.filter(verf_link = verf_link).first()

    if user:
        if user.email_verified == True:
            messages.info(request, "Your account is already verified")
            return render(request, "login.html")
        else:
            user.email_verified = True
            user.save()
            # messages.success(request, "Congratulations! Your account has been verified.")

        return render(request, "verified.html")
    else:
        return render(request, "verf_error.html")



def my_profile(request):
    return render(request, 'user_profile.html')

def updateProfile(request):
    if request.method == "POST":
        user = User.objects.get(username = request.user.username)
        user.username = request.POST['username']
        user.first_name = request.POST['first_name']
        user.last_name = request.POST['last_name']
        user.email = request.POST['email']
        user.mobile_no = request.POST['mobile_no']
        user.save()
        return redirect("my_profile")
    else:
        return render(request, "update_profile.html")

def forget_password(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)
            verf_link = str(uuid.uuid4())
            user.verf_link = verf_link  # Assuming you have a field for the verification link
            user.save()
            send_mail(
                'Reset your password:',
                f"Hello {user.username}! Click on the link to reset your password:\n http://127.0.0.1:8000/account/verifipassword/{verf_link}/",
                EMAIL_HOST_USER,
                [email],
                fail_silently=True
            )
            # messages.success(request, "An email has been sent to your email.")
            # return render(request, 'pass_reset.html')

            return redirect('verify_account')
        else:
            messages.warning(request, 'Account does not exist with this email. Please signup.')
            return render(request, 'signup.html')
    return render(request, 'pass_reset.html')

def verifipassword(request, verf_link):
    user = User.objects.filter(verf_link=verf_link).first()
    if user is None:
        messages.error(request, 'Invalid verification link.')
        return render(request, 'verifypassword.html')

    if request.method == 'POST':
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')
        if pass1 == pass2:
            user.set_password(pass1)
            user.verf_link = ''  # Clear the verification link after use
            user.save()
            return HttpResponse('Password reset successful')
        else:
            messages.error(request, 'Passwords do not match.')
    
    return render(request, 'verifypassword.html')




def changepass(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            fm = PasswordChangeForm(user=request.user, data=request.POST)
            if fm.is_valid():
                fm.save()
                update_session_auth_hash(request, fm.user)  # Important to keep the user logged in
                return redirect('my_profile')
        else:
            fm = PasswordChangeForm(user=request.user)
        return render(request, 'changepass.html', {'form': fm})
    else:
        return redirect('/user_login/')