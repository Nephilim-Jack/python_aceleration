from django import forms
from .models import User


class UserModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        widgets = {
            'password': forms.PasswordInput()
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class': 'fieldsForm'})
        self.fields['username'].label = 'Nome de Usuário'

        self.fields['email'].widget.attrs.update({'class': 'fieldsForm'})
        self.fields['email'].label = 'E-mail'

        self.fields['password'].widget.attrs.update({'class': 'fieldsForm'})
        self.fields['password'].label = 'Senha'
