from django.shortcuts import render, redirect
from django.contrib import messages

from .forms import OwnerModelForm, GuestModelForm

def index(request):
    return render(request, 'index.html', {})

def owner(request):
    form = OwnerModelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = OwnerModelForm(request.POST, request.FILES)
        if form.is_valid():
            owner = form.save()
            messages.success(request, 'Hóspede cadastrado com sucesso!')
            # return redirect('owner-detail', pk=owner.pk) 
        else:
            messages.error(request, 'Erro ao cadastrar hóspede!')
    context = {
        'form': form
    }
    return render(request, 'owner.html', context)

def guest(request):
    form = GuestModelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = GuestModelForm(request.POST, request.FILES)
        if form.is_valid():
            guest = form.save()
            messages.success(request, 'Hóspede cadastrado com sucesso!')
            # return redirect('guest-detail', pk=guest.pk) 
        else:
            messages.error(request, 'Erro ao cadastrar hóspede!')
    context = {
        'form': form
    }
    return render(request, 'guest.html', context)