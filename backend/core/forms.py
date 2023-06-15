from django import forms
import json

from .models import Owner, Guest, Photo

class OwnerModelForm(forms.ModelForm):
    class Meta:
        model = Owner
        fields = ['name', 'cpf', 'password', 'first_access', 'chat_id']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
            'password': forms.PasswordInput(attrs={'class': 'form-control'}),
            'first_access': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'chat_id': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True):
        instance = self.instance
        file = self.cleaned_data.get('file')
        if file:
            photo_instance = Photo(file=file, guest=instance)
            photo_instance.save()
        return super().save(commit=commit)


class GuestModelForm(forms.ModelForm):
    photo = forms.ImageField(label='Foto', required=False)

    class Meta:
        model = Guest
        fields = ['name', 'cpf', 'nickname', 'relationship']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'cpf': forms.TextInput(attrs={'class': 'form-control'}),
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



