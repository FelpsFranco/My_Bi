import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from Analisedados.models import Atendimento, Atendente



atendente1 = Atendente.objects.create(nome='John')
atendente1.save()


registrados = [0, 0, 0, 1, 1, 0, 0, 0, 0, 1, 3, 0, 0, 0, 0, 0, 2, 1, 0, 0, 0, 0, 0, 31, 0, 1, 0, 0, 0, 0]
chamados = []
qtd_positivos = []
qtd_negativos = []


for z, chamado in enumerate(chamados):
    atendimento = Atendimento(
        atendente=atendente1,
        qtd_chamados=chamado,
        qtd_registrados=registrados[z],
        positivos=qtd_positivos[z],
        negativos=qtd_negativos[z],
        data='2023-04-'+str(z+1)
    )
    atendimento.save()




# Mostrar todos
# registros = Atendimento.objects.all()
# for registro in registros:
#     print("Nome:", registro.atendente.nome)
#     print("Quantidade de chamados:", registro.qtd_chamados)
#     print("Quantidade registrada:", registro.qtd_registrados)
#     print("Positivos:", registro.positivos)
#     print("Negativos:", registro.negativos)
#     print("Data:", registro.data)
#     print()

# Deletar Analista e Atendimentos
# analista = Atendente.objects.filter(nome='Larissa')
#
# Atendimento.objects.filter(atendente__in=analista).delete()
#
# analista.delete()