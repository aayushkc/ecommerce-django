
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Product
class UserLoginForm(ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']

class UserRegisterForm(UserCreationForm):
	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user

class AddProduct(ModelForm):
    class Meta:
        model = Product
        fields = ['name', 'image', 'price']