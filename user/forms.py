from django.forms.widgets import FileInput
from django import forms
from .models import Profile
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


#this is Registration Form
class UserRegistrationFrom(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class':'regi-input','placeholder':'Enter Your Fist Name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class':'regi-input','placeholder':'Enter Your Last Name'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'regi-input','placeholder':'Enter Your Password'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class':'regi-input','placeholder':'Confirm Your Password'}))

    class Meta:
        model = User
        fields = ('first_name', 'last_name','username', 'email', 'password1','password2')
        widgets = {
            'username':forms.TextInput(attrs={'class':'regi-input','placeholder':'Enter a username'}),
            'email':forms.EmailInput(attrs={'class':'regi-input','placeholder':'Enter an Email Id'}),
        }


# this is User Form
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email')

#this is Profile Edit Form
class ProfileForm(forms.ModelForm):
    f_name = forms.CharField(widget=forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter Your Fist Name'}))
    l_name = forms.CharField(widget=forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter Your Last Name'}))
    age = forms.IntegerField(widget=forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter Your Age'}))
    city = forms.CharField(widget=forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter Your City'}))
    country = forms.CharField(widget=forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter Your Country'}))

    class Meta:
        model = Profile
        exclude = ('user','id')
        widgets = {
            'username':forms.TextInput(attrs={'class':'profileForm-input','placeholder':'Enter a username'}),
            'email':forms.EmailInput(attrs={'class':'profileForm-input','placeholder':'Enter an Email Id'}),
            'profileImg': FileInput(),
        }

# #Account Validate Form
# class ValidateForm(forms.Form):
#     token = forms.SlugField()

#     token = forms.SlugField(widget=forms.IntegerField(attrs={'class':'regi-input','placeholder':'Enter Your Token'}))