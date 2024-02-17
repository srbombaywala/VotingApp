from django import forms
from django.forms.widgets import TextInput
from .models import member

class UserRegistrationForm(forms.ModelForm):
    class Meta:
        model = member
        fields = ['first_name', 'last_name', 'ppan','picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px; margin: auto;', 'placeholder': 'Enter your First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px; margin: auto;', 'placeholder': 'Enter your Surname'}),
            'ppan': forms.TextInput(attrs={'class': 'form-control','style': 'width: 300px; margin: auto;', 'placeholder': 'Enter your PPAN'}),
            'picture': forms.ClearableFileInput(attrs={'class': 'form-control-file','style': 'width: 300px; margin: auto;'}),
        }
        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'ppan': 'PPAN',
            'picture': 'Profile Picture',
        }

class logintovoteform(forms.Form):
    otp = forms.CharField(max_length=6, label= 'OTP', widget=forms.TextInput(attrs={'class':'form-control','style': 'width: 300px; margin: auto;','type':'number', 'placeholder':'Enter your OTP'}))
    password = forms.CharField(max_length=255, label= 'Password', widget=forms.PasswordInput(attrs={'class':'form-control','style': 'width: 300px; margin: auto;','placeholder': 'Enter the Master Password'}))

class generateotp(forms.Form):
    ppan = forms.CharField(max_length=4, label= 'PPAN', widget=forms.TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'placeholder': 'Enter your PPAN'}))

class votingform(forms.Form):
    field1 = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'id':'field1', 'name':'field1','placeholder':'Field 1'}))
    field2 = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'id':'field2', 'name':'field2','placeholder':'Field 2'}))
    field3 = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'id':'field3', 'name':'field3','placeholder':'Field 3'}))
    field4 = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'id':'field4', 'name':'field4','placeholder':'Field 4'}))
    field5 = forms.CharField(max_length=100, widget=TextInput(attrs={'class': 'form-control', 'style': 'width: 300px; margin: auto;', 'id':'field5', 'name':'field5','placeholder':'Field 5'}))
