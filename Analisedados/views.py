from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import pandas as pd
import random
import datetime as dt


@login_required
def dash(request):
    file = pd.read_excel("./Analisedados/dados/chamados_abril.xlsx")
    analistas = file['Analista'].tolist()
    chamados = file['Chamados'].tolist()

    data = [['Analista', 'Chamados']]
    colors = []
    for analista, chamado in zip(analistas, chamados):
        color = '#' + ''.join(random.choices('0123456789abcdef', k=6))
        data.append([analista, chamado])
        colors.append(color)
    datetime = dt.datetime.now()
    formatted_date = datetime.strftime('%Y-%m-%d')
    infor = {
        'data': data,
        'colors': colors,
        'datetime': formatted_date
    }
    print(infor['datetime'])
    return render(request, "Analisedados/dash.html", infor)


# Create your views here.
def index(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dash')
            else:
                messages.error(request, 'Credenciais inválidas!')
    else:
        form = LoginForm()

    return render(request, 'Analisedados/index.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect(reverse('index'))
