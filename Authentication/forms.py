from django import forms
from .models import Account
from .models import UserProfile


class RegistrationalForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'Enter Password',
        'class':'form-control',
    }
    ))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder':'confirm Password',
       
    }
    ))

    class Meta:
        model = Account
        fields = ['first_name','last_name','phone_number','email','password']

    
    def __init__(self, *args, **kwargs):
        super(RegistrationalForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Enter First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Enter Last Name'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Enter Phone Number'
        self.fields['email'].widget.attrs['placeholder'] = 'Enter Email Address'
        
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    def clean(self):
        cleaned_data = super(RegistrationalForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                'password does not match!'
            )


class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter Email',
        'class': 'form-control',
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password',
        'class': 'form-control',
    }))



# user profile and views are here

class UserForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = ('first_name', 'last_name', 'phone_number')
        widgets = {
                    'first_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'last_name' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'phone_number':forms.TextInput(attrs={'class':'form-control col-12'}),    
        }
                    
        


class UserProfileForm(forms.ModelForm):
    profile_picture=forms.ImageField(required=False, error_messages= {'invalid':{"Image files only"}},widget=forms.FileInput)
    class Meta:

        model = UserProfile
        fields = ('address_line_1','address_line_2','city','state','country','profile_picture')
        widgets = {
                    'address_line_1' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'address_line_2' : forms.TextInput(attrs={'class':'form-control col-12'}),
                    'city':forms.TextInput(attrs={'class':'form-control col-12'}), 
                    'state':forms.TextInput(attrs={'class':'form-control col-12'}),
                    'country':forms.TextInput(attrs={'class':'form-control col-12'}),
                    
                    

        }