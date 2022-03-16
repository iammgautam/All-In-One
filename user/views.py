import threading

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import (DjangoUnicodeDecodeError, force_bytes,
                                   force_str)
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from email_validator import validate_email

from .forms import ProfileForm, UserRegistrationFrom
from .models import Profile
from .utils import generate_token


class EmailThread(threading.Thread):
    def __init__(self, email_message):
        self.email_message = email_message
        threading.Thread.__init__(self)

    def run(self):
        self.email_message.send()

# Create your views here.

# this is loginPage function
def loginPage(request):

    if request.user.is_authenticated:
        return redirect('profile')
    # if the method is POST in form then...
    if request.method == 'POST':
        # take username, password in a seperate variable.
        username = request.POST['username']
        password = request.POST['password']

        # use try /expect block to check if the username is correct or not
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Account doesn't exist")
            return redirect('home')

        # if correct username then it will authenticate it with password
        user = authenticate(request, username=username, password=password)

        # if authentication is correct i.e.,((user !=None))
        if user is not None:
            if user.is_active == False:
                messages.error(request, 'Please confirm your email')
                return redirect('home')
            login(request, user)  # we login using login() in-built function.
            messages.success(request, f'Hi {username}👋,Welcome to ZengoChat')
            return redirect('home')
        else:
            messages.error(request, "Username or Password is Incorrect👀")
            return redirect('home')

    return render(request, 'home.html')

# function for logout of the user.
def logoutPage(request):
    # in-built function for the logout.(which deletes the session)
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('home')

# function for registering a new User.
def registerPage(request):

    if request.user.is_authenticated:
        return redirect('home')

    # instance of in-built UserCreationForm()
    form = UserRegistrationFrom()
    if request.method == 'POST':
        form = UserRegistrationFrom(request.POST)
        # takes the input email of the user
        post_email = request.POST.get('email')
        # checks if the email already exsit or not.
        if Profile.objects.filter(email=post_email).exists():
            messages.error(request, "Email already exists")
            return redirect('register')

        if form.is_valid():
            # save the form in user variable where commit=False tells not to completely save it.
            user = form.save(commit=False)
            username = user.username
            # save all the username in lowercase for uniqueness.
            user.username = user.username.lower()
            user.is_active = False
            user.save()

            ### Email Validation Part ###
            # first get the current site adress
            currect_site = get_current_site(request)
            # have a email_subject to send
            email_subject = 'Activate your Account'
            # compose a email message which we will render in html form
            message = render_to_string('user/email/activate.html',
                                       {
                                           'user': user,
                                           'domain': currect_site,
                                           'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                           'token': generate_token.make_token(user),
                                       }
                                       )
            # use EmailMessage() in-built function in Django to compane overall email
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [post_email],
            )
            # use .send() to send the email
            # email_message.send()
            EmailThread(email_message).start()
            messages.success(request, f'Hi {username},👋 Confirm your Email For Confirmation.')
            return redirect('home')
        else:
            messages.error(request, 'Error Occured During Registration!!')
    context = {'forms': form}
    return render(request, 'user/register.html', context)


# activate User Email
class activateEmail(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as identifier:
            user = None

        if user is not None and generate_token.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(request, "Email Validated, Welocome")
            return redirect('home')

        if user is not None and user.is_active == True:
            return render(request, 'error.html', status=404)

# password reset function
class RequestResetPass(View):
    def get(self, request):
        return render(request, 'home.html')

    def post(self, request):
        email = request.POST['email']

        if not validate_email(email):
            messages.error(request, 'Invalid Email')
            return redirect('home')

        user = User.objects.filter(email=email)
        if user.exists():

            ### Email Validation Part ###
            # first get the current site adress
            currect_site = get_current_site(request)
            # have a email_subject to send
            email_subject = 'Password Reset for ZengoChat'
            # compose a email message which we will render in html form
            message = render_to_string('user/email/resetPass.html',
                                       {
                                           'user': user,
                                           'domain': currect_site,
                                           'uid': urlsafe_base64_encode(force_bytes(user[0].pk)),
                                           'token':PasswordResetTokenGenerator().make_token(user[0]),
                                       }
                                       )
            # use EmailMessage() in-built function in Django to compane overall email
            email_message = EmailMessage(
                email_subject,
                message,
                settings.EMAIL_HOST_USER,
                [email],
            )

            # use .send() to send the email
            # email_message.send()
            EmailThread(email_message).start()
            messages.success(request, 'Check out your Email')
            return render(request, 'home.html')

        if not user.exists():
            messages.success(request, 'Email doesn\'t Exist')
            return render(request, 'home.html')
        

#New Password Validation Function
class new_password(View):
    def get(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
        }
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)

            if not PasswordResetTokenGenerator().check_token(user,token):
                messages.error(request, 'Password reset link is invalid, please request a new one.')
                return redirect('home')
            
            return render(request, 'user/email/newPassword.html', context)

        except DjangoUnicodeDecodeError  as identifier:
            messages.success(request, "Invalid Link")
            return redirect('home')

    def post(self, request, uidb64, token):
        context = {
            'uidb64':uidb64,
            'token':token,
            'has_error':False,
        }
        password = request.POST.get('password')
        password2 = request.POST.get('password1')
        if len(password) < 8:
            messages.error(request, "Password should be at least 8 characters long")
            context['has_error']= True
        if password != password2:
            messages.error(request, "Password don\'t match")
            context['has_error']= True
        if context['has_error'] == True:
            return render(request, 'user/email/newpassword.html', context)

        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=uid)
            user.set_password(password)
            user.save()

            messages.success(request, 'Password reset Successfully.')
            return redirect('home')
        
        except DjangoUnicodeDecodeError as identifier:
            messages.error(request,"Something Went Wrong")
            return render(request, 'user/email/newPassword.html', context)

# this is profile's Edit form function
@login_required
def profileEdit(request):
    if request.method == 'POST':
        p_form = ProfileForm(request.POST, request.FILES,
                             instance=request.user.profile)
        if p_form.is_valid:
            p_form.save()
            return redirect('profile')
    else:
        p_form = ProfileForm(instance=request.user.profile)

    return render(request, 'user/profileEdit.html', {'p_form': p_form})


# the profile page function
@login_required
def profile(request):
    profile = request.user.profile
    context = {
        'profile': profile
    }
    return render(request, 'user/profile.html', context)

# the main page function
def home(request):
    return render(request, 'home.html')
