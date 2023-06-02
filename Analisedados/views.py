from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import datetime as dt
from django.db.models import Sum
from Analisedados.models import Atendimento, Atendente
from datetime import datetime, timedelta


def busca_info(request):
    if 'initial-date-inp' in request.GET and 'final-date-inp' in request.GET:
        date_initial = request.GET.get('initial-date-inp')
        date_final = request.GET.get('final-date-inp')
        try:
            dI = dt.datetime.strptime(date_initial, '%Y-%m-%d')
            dF = dt.datetime.strptime(date_final, '%Y-%m-%d')
        except ValueError:
            messages.error(request, 'Formato de data inválido.')
            return redirect('graphics')
        quality = graphics_quality(dI, dF)
        percent = percent_graphic(dI, dF)
        mounth = mounth_total(dI, dF)
        atendentes_filtrados = Atendente.objects.filter(atendimento__data__range=[dI, dF]).annotate(total_chamados=Sum('atendimento__qtd_chamados')).annotate(total_registros=Sum('atendimento__qtd_registrados'))
        if atendentes_filtrados is None:
            atendentes_filtrados = 0

        analistas_filtrados = [atendente.nome for atendente in atendentes_filtrados]
        chamados_filtrados = [atendente.total_chamados or 0 for atendente in atendentes_filtrados]
        registrados_filtrados = [atendente.total_registros or 0 for atendente in atendentes_filtrados]

        data = [['Analista', 'Jivo', 'ERP']]
        for analista, chamado, registrado in zip(analistas_filtrados, chamados_filtrados, registrados_filtrados):
            data.append([analista, chamado, registrado])
        formatted_di = dI.strftime('%Y-%m-%d')
        formatted_df = dF.strftime('%Y-%m-%d')
        infor = {
            'data_inicial': formatted_di,
            'data_final': formatted_df,
            'data': data,
            'quality': quality,
            'percent': percent,
            'mouth': mounth,
        }
        return infor


    else:
        atendentes = Atendente.objects.annotate(total_chamados=Sum('atendimento__qtd_chamados'))
        atendentes_chamados = Atendente.objects.annotate(total_registros=Sum('atendimento__qtd_registrados'))
        analistas = [atendente.nome for atendente in atendentes]
        chamados = [atendente.total_chamados for atendente in atendentes]
        registrados = [atendente.total_registros for atendente in atendentes_chamados]
        quality = graphics_quality_not_form()
        percent = percent_graphic_not_validate_data()
        mounth = mounth_total_not_validate_data()
        data = [['Analista', 'Jivo', 'ERP']]
        for analista, chamado, registrado in zip(analistas, chamados, registrados):
            data.append([analista, chamado, registrado])
        formatted_di = '2023-04-01'
        formatted_df = '2023-05-31'
        infor = {
            'data_inicial': formatted_di,
            'data_final': formatted_df,
            'quality': quality,
            'data': data,
            'percent': percent,
            'mouth': mounth,
        }
        return infor


@login_required
def dash(request):
    module = busca_info(request)
    return render(request, "Analisedados/dash.html", module)


@login_required
def graphics(request):
    infor = busca_info(request)
    return render(request, "Analisedados/graphics.html", infor)


def percent_graphic(dI, dF):
    delta = dF - dI
    chamados_por_dia = [['Dia', 'Total Chamados']]

    for i in range(delta.days + 1):
        current_date = dI + timedelta(days=i)
        formatted_date = current_date.strftime('%d')
        chamados = Atendimento.objects.filter(data=current_date).aggregate(total_chamados=Sum('qtd_chamados'))
        chamados_por_dia.append([formatted_date, chamados['total_chamados'] or 0])

    return chamados_por_dia


def mounth_total(dI, dF):
    delta = dF - dI
    chamados_por_mes = [['Mês', 'Total Chamados']]
    meses_processados = set()

    for i in range(delta.days + 1):
        current_date = dI + timedelta(days=i)
        formatted_month = current_date.strftime('%B')

        if formatted_month not in meses_processados:
            chamados = Atendimento.objects.filter(data__year=current_date.year, data__month=current_date.month).aggregate(total_chamados=Sum('qtd_chamados'))
            chamados_por_mes.append([formatted_month, chamados['total_chamados'] or 0])
            meses_processados.add(formatted_month)

    return chamados_por_mes


def mounth_total_not_validate_data():
    dI = '2023-04-01'
    dF = '2023-05-31'

    formatted_dI = datetime.strptime(dI, '%Y-%m-%d')
    formatted_dF = datetime.strptime(dF, '%Y-%m-%d')

    delta = formatted_dF - formatted_dI
    chamados_por_mes = [['Mês', 'Total Chamados']]
    meses_processados = set()

    for i in range(delta.days + 1):
        current_date = formatted_dI + timedelta(days=i)
        formatted_month = current_date.strftime('%B')

        if formatted_month not in meses_processados:
            chamados = Atendimento.objects.filter(data__year=current_date.year, data__month=current_date.month).aggregate(total_chamados=Sum('qtd_chamados'))
            chamados_por_mes.append([formatted_month, chamados['total_chamados'] or 0])
            meses_processados.add(formatted_month)

    return chamados_por_mes


def percent_graphic_not_validate_data():
    dI = '2023-04-01'
    dF = '2023-05-31'

    formatted_dI = datetime.strptime(dI, '%Y-%m-%d')
    formatted_dF = datetime.strptime(dF, '%Y-%m-%d')

    delta = formatted_dF - formatted_dI
    chamados_por_dia = [['Dia', 'Total Chamados']]

    for i in range(delta.days + 1):
        current_date = formatted_dI + timedelta(days=i)
        formatted_date = current_date.strftime('%d')
        chamados = Atendimento.objects.filter(data=current_date).aggregate(total_chamados=Sum('qtd_chamados'))
        chamados_por_dia.append([formatted_date, chamados['total_chamados'] or 0])

    return chamados_por_dia


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
