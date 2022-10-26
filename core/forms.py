from django import forms
from django.forms import ValidationError
from .models import GeneralLink
#  Error()

class GeneralLinkForm(forms.ModelForm):

    class Meta:
        model = GeneralLink
        fields = [
            'name',
            'url',
            'photo',
            'section',
            'type',
            'description',
            'short_description',
            'tools',
            'company',
            'language'

            ] # ('name', 'description', 'url')

     

    # def clean_description(self):
    #     description = self.cleaned_data['description']
    #     if len(description.split()) < 3:
    #         raise ValidationError('Izoh kamida 3 ta so\'zdan iborat bo\'lishi kerak.')
        
    #     return description

    # def clean(self):
    #     super().clean()
    #     url_data = self.cleaned_data['url']
    #     if Link.objects.filter(url=url_data).exists():
    #         raise ValidationError('Bunday havola allaqachon qo\'shilgan')
        
    #     return self.cleaned_data


class RegisterForm(forms.Form):
    username = forms.CharField(max_length=120, required=True, label='Login')
    email = forms.EmailField(max_length=50, initial='example@gmail.com',
             help_text='Iltimos to\'g\'ri email kiriting.')
    password = forms.CharField(max_length=100,
                        widget=forms.PasswordInput(attrs={'class': 'special'}))
    password_confirmation = forms.CharField(max_length=100, widget=forms.PasswordInput)
    # description = forms.CharField(max_length=5000, widget=forms.Textarea)

    password_confirmation.widget.attrs.update({'class': 'special'})
    password_confirmation.widget.attrs.update(size='40')

    def clean_password(self):
        parol = self.cleaned_data['password']
        if len(parol) < 7:
            raise ValidationError('Parol kamida 7ta belgidan iborat bo\'lishi lozim')
        if parol.isnumeric():
            raise ValidationError('Parolda kamida bitta harf yoki belgi ishtirok etishi lozim')
        if parol.isalpha():
            raise ValidationError('Parolda kamida bitta raqam ishtirok etishi lozim')
        return parol

    def clean_password_confirmation(self):
        # password = self.cleaned_data['password']
        print(self.data)
        password = self.data['password']
        confirm_password = self.cleaned_data['password_confirmation']
        if password != confirm_password:
            raise ValidationError('Tasdiqlash paroli notogri')
        return confirm_password

    def clean(self):
        data = super().clean() # cleaned_data
        if data['username'] in usernames:
            raise ValidationError('This username is already registered on our platform')
        return data
