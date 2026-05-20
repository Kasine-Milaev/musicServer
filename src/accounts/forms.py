from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
User = get_user_model()

class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ("username", "email")

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже занят другим пользователем.")
        return email
    
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email','first_name', 'last_name','cover']

    def clean_email(self):
        email = self.cleaned_data.get('email')

        validator = EmailValidator(message="Неверный формат Email адреса")

        try:
            validator(email)
        except ValidationError as e:
            raise forms.ValidationError(e.message)

        if User.objects.filter(email__iexact=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Этот email уже занят другим пользователем.")
        return email