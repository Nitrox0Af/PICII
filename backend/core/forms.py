from django import forms
<<<<<<< HEAD
import json
=======
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
>>>>>>> fe80b15df7c6dbf484fcf184382bb80c223f5684

from .models import Guest, Photo, CustomUser


class CustomUserCreateForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')
        labels = {'username': 'E-mail'}

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        user.email = self.cleaned_data["username"]
        if commit:
            user.save()
        return user


class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name')


class GuestModelForm(forms.ModelForm):
    photo = forms.ImageField(label='Foto', required=False)

    class Meta:
        model = Guest
        fields = ['name', 'email', 'nickname', 'relationship']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'nickname': forms.TextInput(attrs={'class': 'form-control'}),
            'relationship': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def save(self, commit=True):
        instance = super().save(commit=False)
        data = json.loads(self.data['guest'])
        instance.name = data.get('name')
        instance.cpf = data.get('cpf')
        instance.nickname = data.get('nickname')
        instance.relationship = data.get('relationship')
        

        if commit:
            instance.save()

        file = self.cleaned_data.get('photo')
        if file:
            photo_instance = Photo(file=file, guest=instance)
            photo_instance.save()

        return instance



