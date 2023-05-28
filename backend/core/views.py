import os
from django.conf import settings
from django.shortcuts import render, redirect
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, FileResponse

from .forms import OwnerModelForm, GuestModelForm


def index(request):
    return render(request, 'index.html', {})


def owner(request):
    print(f'Usuario: {request.user}')
    form = OwnerModelForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        form = OwnerModelForm(request.POST, request.FILES)
        if form.is_valid():
            owner = form.save()
            messages.success(request, 'Proprietario cadastrado com sucesso!')
            # return redirect('owner-detail', pk=owner.pk) 
        else:
            messages.error(request, 'Erro ao cadastrar Proprietario!')
    context = {
        'form': form
    }
    return render(request, 'owner.html', context)


def guest(request):
    print(f'Usuario: {request.user}')
    if str(request.user) != 'AnonymousUser':
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
    else:
        return redirect('index')


def encoding(request, filename):
    try:
        encoding_path = os.path.join(settings.MEDIA_ROOT, 'encoding', f'{filename}.pkl')

        if os.path.exists(encoding_path):
            with open(encoding_path, 'rb') as file:
                response = HttpResponse(file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{filename}.pkl"'
                return response
        else:
            messages.error(request, 'O arquivo de encoding não existe.')
            return redirect('index')
    except Exception:
        messages.error(request, 'Ocorreu um erro durante o download do arquivo.')
        return redirect('index')