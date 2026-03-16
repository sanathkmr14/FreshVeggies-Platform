from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, PasswordResetForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from django.contrib.auth  import password_validation
from .models import Customer

class CustomerRegistrationForm(UserCreationForm):
    password1=forms.CharField(label='Password', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password' }))
    password2=forms.CharField(label='Confirm Password again', widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder':'Enter Password again'}))
    first_name=forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter First Name'}))
    last_name=forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Enter Last Name'}))
    email=forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder':'Enter Email'  }))
    class Meta:
        model= User
        fields=['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
        labels={'email':'Email'}
        widgets={'username': forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Enter Username'})}

#class LoginForm(AuthenticationForm):
   # username=UsernameField(widget=forms.TextInput(attrs={'autofocus':'True','class':'form-contrl'}))
   # password=forms.CharField(label=("password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password','class':'form-contrl'}))

class LoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'})
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
    )

#class MyPasswordChangeForm(PasswordChangeForm):
    #old_password=forms.CharField(label=("Old Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-contrl'}))
    #new_password1=forms.CharField(label=("New Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-contrl'})),
    #help_text=password_validation.password_validators_help_text_html()
    #new_password2=forms.CharField(label=("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-contrl'}))

class MyPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

#class MyPasswordResetForm(PasswordResetForm):
   #email=forms.EmailField(label=("Email"), max_length=254, widget=forms.EmailInput(attrs={'autocomplete':'email','class':'form-control', 'placeholder':'Enter Email'  })),

class MyPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label='Email', max_length=254, widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}))

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError('Please enter your email address.')
        return email


class MySetPasswordForm(SetPasswordForm):
    #new_password1=forms.CharField(label=("New Password"), widget=forms.PasswordInput(attrs={'autocomplete':'current-password',  'class':'form-contrl'})),
    #help_text=password_validation.CommonPasswordValidator()
    #new_password2=forms.CharField(label=("Confirm Password"), strip=False, widget=forms.PasswordInput(attrs={'autocomplete':'current-password', 'autofocus':True, 'class':'form-contrl'}))
    
    new_password1 = forms.CharField(
       label='New Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )
    new_password2 = forms.CharField(
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={'class': 'form-control'})
    )

class CustomerProfileForm(forms.ModelForm):
    class Meta:
      model = Customer
      fields = ['name', 'address', 'city', 'state', 'zipcode']
      labels = {
          'address': 'Address',
      }
      widgets ={
                'name':forms.TextInput(attrs={'class':'form-control'}),
                'address': forms.TextInput(attrs={'class':'form-control'}),
                'city': forms.TextInput(attrs={'class':'form-control'}), 
                'state':forms.Select(attrs={'class':'form-control'}),
                'zipcode': forms.NumberInput(attrs={'class': 'form-control'}),
            }

class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(label='First Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        labels = {'first_name': 'First Name', 'last_name': 'Last Name', 'email': 'Email'}
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }

class UserProfileUpdateForm(forms.Form):
    phone = forms.CharField(
        label='Phone Number',
        max_length=20,
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter Phone Number'})
    )
