from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
from django_quill.forms import QuillFormField
class RegisterUserForm(UserCreationForm):
	email = forms.EmailField(widget=forms.EmailInput(attrs={'class':'form-control'}))
	first_name = forms.CharField(max_length=80,widget=forms.TextInput(attrs={'class':'form-control'}))
	last_name = forms.CharField(max_length=80,widget=forms.TextInput(attrs={'class':'form-control'}))

	class Meta:
		model = User
		fields = ('username', 'first_name', "last_name", 'email', 'password1','password2')

	def __init__(self, *args, **kwargs):
		super(RegisterUserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['password1'].widget.attrs['class'] = 'form-control'
		self.fields['password2'].widget.attrs['class'] = 'form-control'

class updateUser(forms.ModelForm):
	pass

class ProfileForm(forms.ModelForm):
		
	class Meta:
		model = Profile
		fields = ('profile_pic', 'bio', 'number')
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)
		self.fields['profile_pic'].widget.attrs['class'] = 'form-control'
		self.fields['bio'].widget.attrs['class'] = 'form-control'
		self.fields['number'].widget.attrs['class'] = 'form-control'

class UserForm(UserChangeForm):
	class Meta:
		model = User
		fields = ('username', 'first_name', "last_name", 'email','password')

	def __init__(self, *args, **kwargs):
		super(UserForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['class'] = 'form-control'
		self.fields['first_name'].widget.attrs['class'] = 'form-control'
		self.fields['last_name'].widget.attrs['class'] = 'form-control'
		self.fields['email'].widget.attrs['class'] = 'form-control'