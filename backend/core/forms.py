from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

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
    photo = forms.ImageField(label='Foto', required=True)

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
        instance = self.instance
        file = self.cleaned_data.get('file')
        if file:
            photo_instance = Photo(file=file, guest=instance)
            photo_instance.save()
        return super().save(commit=commit)



