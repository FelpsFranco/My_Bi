from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import LoginForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
import pandas as pd


@login_required
def dash(request):
    file = pd.read_csv("./dados/Chamados_abril.xlsx")

    return render(request, "Analisedados/dash.html")


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
