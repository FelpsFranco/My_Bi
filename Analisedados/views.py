from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import random
import datetime as dt
from django.db.models import Sum
from Analisedados.models import Atendimento, Atendente

@login_required
def graphics(request):
    if 'initial-date-inp' in request.GET and 'final-date-inp' in request.GET:
        date_initial = request.GET.get('initial-date-inp')
        date_final = request.GET.get('final-date-inp')
        dI = dt.datetime.strptime(date_initial, "%Y-%m-%d")
        dF = dt.datetime.strptime(date_final, "%Y-%m-%d")

        atendentes_filtrados = Atendente.objects.filter(atendimento__data__range=[dI, dF]).annotate(total_chamados=Sum('atendimento__qtd_chamados')).annotate(total_registros=Sum('atendimento__qtd_registrados'))
        analistas_filtrados = [atendente.nome for atendente in atendentes_filtrados]
        chamados_filtrados = [atendente.total_chamados or 0 for atendente in atendentes_filtrados]
        registrados_filtrados = [atendente.total_registros or 0 for atendente in atendentes_filtrados]

        data = [['Analista', 'Chamados', 'Registrados']]
        colors = []
        for analista, chamado, registrado in zip(analistas_filtrados, chamados_filtrados, registrados_filtrados):
            color = '#' + ''.join(random.choices('0123456789abcdef', k=6))
            data.append([analista, chamado, registrado])
            colors.append(color)
        datetime = dt.datetime.now()
        formatted_date = datetime.strftime('%Y-%m-%d')
        infor = {
            'dI': dI,
            'dF': dF,
            'data': data,
            'colors': colors,
            'datetime': formatted_date
        }
        return render(request, "Analisedados/graphics.html", infor)

    else:
        atendentes = Atendente.objects.annotate(total_chamados=Sum('atendimento__qtd_chamados'))
        atendentes_chamados = Atendente.objects.annotate(total_registros=Sum('atendimento__qtd_registrados'))
        analistas = [atendente.nome for atendente in atendentes]
        chamados = [atendente.total_chamados for atendente in atendentes]
        registrados = [atendente.total_registros for atendente in atendentes_chamados]

        data = [['Analista', 'Chamados', 'Registrados']]
        colors = []
        for analista, chamado, registrado in zip(analistas, chamados, registrados):
            color = '#' + ''.join(random.choices('0123456789abcdef', k=6))
            data.append([analista, chamado, registrado])
            colors.append(color)
        datetime = dt.datetime.now()
        formatted_date = datetime.strftime('%Y-%m-%d')
        infor = {
            'data': data,
            'colors': colors,
            'datetime': formatted_date
        }
        return render(request, "Analisedados/graphics.html", infor)


@login_required
def dash(request):
    return render(request, "Analisedados/dash.html")


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
