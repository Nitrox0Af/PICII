import os
import subprocess
from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.shortcuts import redirect
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .forms import GuestModelForm
from .models import Guest, Access, CustomUser


def index(request):
    return render(request, 'index.html', {})


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


def guest_json(request, email):
    guest = get_object_or_404(Guest, email=email)
    guest_data = {
        'name': guest.name,
        'email': guest.email,
        'nickname': guest.nickname,
        'relationship': guest.relationship,
        'owner': guest.owner.email
    }
    access = Access(guest=guest)
    access.save()
    return JsonResponse(guest_data)


@csrf_exempt
def owner_json(request, email):
    owner = get_object_or_404(CustomUser, email=email)
    if request.method == 'POST':
        chat_id = request.POST.get('chat_id')
        owner.chat_id = chat_id
        owner.first_access = False
        owner.save()

    owner_data = {
        'name': owner.get_full_name(),
        'email': owner.email,
        'first_access': owner.first_access,
        'chat_id': owner.chat_id
    }
    return JsonResponse(owner_data)


def telegram(request):
    return render(request, 'telegram.html', {})


def telegram_bot(request) -> None:
    command = ["python", "./core/telegram_bot.py"]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode == 1:
        print("Sucesso")
    else:
        print("Error:")
        print(result.stderr)
    return redirect('index')


@csrf_exempt
def create_guest(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        nickname = request.POST.get('nickname')
        relationship = request.POST.get('relationship')

        guest = Guest(name=name, email=email, nickname=nickname, relationship=relationship)
        guest.save()

        guest_data = {
            'name': guest.name,
            'email': guest.email,
            'nickname': guest.nickname,
            'relationship': guest.relationship,
        }
        return JsonResponse(guest_data)

    return JsonResponse({'message': 'Método não permitido'}, status=405)