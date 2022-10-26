from django import forms
from django.forms.widgets import PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from users.models import User

class LoginForm(forms.Form):
    
    email = forms.EmailField(required=True) # error_messages={"required": "", "invalid": ""}
    password = forms.CharField(required=True, widget=PasswordInput)

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ushbu email tizimda ro\'yxatdan o\'tkazilmagan.')
        return email
    
    def clean_password(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data['password']
        if email:
            user = User.objects.filter(email=email).first()
            if user:
                if not user.check_password(password):
                    raise forms.ValidationError('Parol notog\'ri kiritildi.')
        return password


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(max_length=120, required=True, label='Elektron Pochta')
    password = forms.CharField(max_length=100, label='Parol',
                        widget=forms.PasswordInput(attrs={'class': 'special'}))
    password_confirmation = forms.CharField(max_length=100, label='Parolni tasdiqlash',
                        widget=forms.PasswordInput)
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'password']
        labels = {
            'first_name': 'Ism',
            'last_name': 'Familiya'
        }
    # password_confirmation.widget.attrs.update({'class': 'special'})
    # password_confirmation.widget.attrs.update(size='40')

    def clean_password(self):
        parol = self.cleaned_data['password']
        if len(parol) < 7:
            raise forms.ValidationError('Parol kamida 7ta belgidan iborat bo\'lishi lozim')
        if parol.isnumeric():
            raise forms.ValidationError('Parolda kamida bitta harf yoki belgi ishtirok etishi lozim')
        if parol.isalpha():
            raise forms.ValidationError('Parolda kamida bitta raqam ishtirok etishi lozim')
        return parol

    def clean_password_confirmation(self):
        password = self.data['password']
        confirm_password = self.cleaned_data['password_confirmation']
        if password != confirm_password:
            raise forms.ValidationError('Tasdiqlash paroli notogri')
        return confirm_password

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ushbu email sistemada ro\'yxatdan o\'tkazilgan.')
        return email


class PasswordResetForm(forms.Form):
    
    email = forms.EmailField(required=True)  

    def clean_email(self):
        email = self.cleaned_data['email']
        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError('Ushbu email tizimda ro\'yxatdan o\'tkazilmagan.')
        return email


class PasswordChangeForm(forms.Form):
    password = forms.CharField(max_length=100, label='Parol',
                        widget=forms.PasswordInput(attrs={'class': 'special'}))
    password2 = forms.CharField(max_length=100, label='Parolni tasdiqlash',
                        widget=forms.PasswordInput)

    def clean_password(self):
        parol = self.cleaned_data['password']
        if len(parol) < 7:
            raise forms.ValidationError('Parol kamida 7ta belgidan iborat bo\'lishi lozim')
        if parol.isnumeric():
            raise forms.ValidationError('Parolda kamida bitta harf yoki belgi ishtirok etishi lozim')
        if parol.isalpha():
            raise forms.ValidationError('Parolda kamida bitta raqam ishtirok etishi lozim')
        return parol

    def clean_password2(self):
        password = self.data['password']
        confirm_password = self.cleaned_data['password2']
        if password != confirm_password:
            raise forms.ValidationError('Tasdiqlash paroli notogri')
        return confirm_password
