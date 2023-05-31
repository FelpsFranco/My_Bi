from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime as dt
from django.db.models import Sum
from Analisedados.models import Atendimento, Atendente


@login_required
def graphics(request):
    if 'initial-date-inp' in request.GET and 'final-date-inp' in request.GET:
        date_initial = request.GET.get('initial-date-inp')
        date_final = request.GET.get('final-date-inp')
        print(date_initial, date_final)
        dI = dt.datetime.strptime(date_initial, '%Y-%m-%d')
        dF = dt.datetime.strptime(date_final, '%Y-%m-%d')
        quality = graphics_quality(dI, dF)
        atendentes_filtrados = Atendente.objects.filter(atendimento__data__range=[dI, dF]).annotate(total_chamados=Sum('atendimento__qtd_chamados')).annotate(total_registros=Sum('atendimento__qtd_registrados'))
        if atendentes_filtrados is None:
            atendentes_filtrados = 0

        analistas_filtrados = [atendente.nome for atendente in atendentes_filtrados]
        chamados_filtrados = [atendente.total_chamados or 0 for atendente in atendentes_filtrados]
        registrados_filtrados = [atendente.total_registros or 0 for atendente in atendentes_filtrados]

        data = [['Analista', 'Jivo', 'ERP']]
        for analista, chamado, registrado in zip(analistas_filtrados, chamados_filtrados, registrados_filtrados):
            data.append([analista, chamado, registrado])
        datetime = dt.datetime.now()
        formatted_di = dI.strftime('%Y-%m-%d')
        formatted_df = dF.strftime('%Y-%m-%d')
        infor = {
            'data_inicial': formatted_di,
            'data_final': formatted_df,
            'data': data,
            'quality': quality,
        }
        return render(request, "Analisedados/graphics.html", infor)


    else:
        atendentes = Atendente.objects.annotate(total_chamados=Sum('atendimento__qtd_chamados'))
        atendentes_chamados = Atendente.objects.annotate(total_registros=Sum('atendimento__qtd_registrados'))
        analistas = [atendente.nome for atendente in atendentes]
        chamados = [atendente.total_chamados for atendente in atendentes]
        registrados = [atendente.total_registros for atendente in atendentes_chamados]
        quality = graphics_quality_not_form()
        data = [['Analista', 'Jivo', 'ERP']]
        for analista, chamado, registrado in zip(analistas, chamados, registrados):
            data.append([analista, chamado, registrado])
        datetime = dt.datetime.now()
        formatted_date = datetime.strftime('%Y-%m-%d')
        formatted_di = formatted_date
        formatted_df = formatted_date
        infor = {
            'data_inicial': formatted_di,
            'data_final': formatted_df,
            'quality': quality,
            'data': data,
        }
        return render(request, "Analisedados/graphics.html", infor)


def graphics_quality(dI, dF):
    atendentes_filtrados = Atendente.objects.filter(atendimento__data__range=[dI, dF]).annotate(total_chamados=Sum('atendimento__positivos')).annotate(total_registros=Sum('atendimento__negativos'))
    if atendentes_filtrados is None:
        atendentes_filtrados = 0
    analistas_filtrados = [atendente.nome for atendente in atendentes_filtrados]
    positivos_filtrados = [atendente.total_chamados or 0 for atendente in atendentes_filtrados]
    negativos_filtrados = [atendente.total_registros or 0 for atendente in atendentes_filtrados]

    quality = [['Analista', 'Positivos', 'Negativos']]
    for analista, positivo, negativo in zip(analistas_filtrados, positivos_filtrados, negativos_filtrados):
        quality.append([analista, positivo, negativo])

    return quality


def graphics_quality_not_form():
    atendentes = Atendente.objects.annotate(total_positivos=Sum('atendimento__positivos'))
    atendentes_chamados = Atendente.objects.annotate(total_negativos=Sum('atendimento__negativos'))
    analistas = [atendente.nome for atendente in atendentes]
    positivos = [atendente.total_positivos for atendente in atendentes]
    negativos = [atendente.total_negativos for atendente in atendentes_chamados]

    quality = [['Analista', 'Positivos', 'Negativos']]
    for analista, chamado, registrado in zip(analistas, positivos, negativos):
        quality.append([analista, chamado, registrado])
    return quality


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
