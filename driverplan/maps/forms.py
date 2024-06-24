from django import forms
from django.contrib.auth.models import User

class RegistroForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super(RegistroForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class RouteForm(forms.Form):
    start = forms.CharField(label='Starting Point', max_length=100)
    end = forms.CharField(label='Destination', max_length=100)
    rate = forms.DecimalField(label='Rate per km', max_digits=10, decimal_places=2)
