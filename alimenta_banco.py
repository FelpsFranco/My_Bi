import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
django.setup()

from Analisedados.models import Atendimento, Atendente



# atendente1 = Atendente.objects.create(nome='Thomas')
# atendente1.save()
#
#
# registrados = [0, 0, 8, 10, 5, 11, 0, 0, 0, 9, 9, 8, 9, 7, 0, 0, 10, 8, 7, 9, 0, 0, 0, 9, 6, 6, 11, 9, 0, 0]
# chamados = [0, 0, 7, 10, 2, 5, 0, 0, 0, 8, 7, 7, 7, 6, 0, 0, 6, 6, 4, 5, 0, 0, 0, 7, 4, 5, 8, 5, 0, 0]
# qtd_positivos = [0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 0, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0]
# qtd_negativos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
#
#
# for z, chamado in enumerate(chamados):
#     atendimento = Atendimento(
#         atendente=atendente1,
#         qtd_chamados=chamado,
#         qtd_registrados=registrados[z],
#         positivos=qtd_positivos[z],
#         negativos=qtd_negativos[z],
#         data='2023-04-'+str(z+1)
#     )
#     atendimento.save()




# Mostrar todos
registros = Atendimento.objects.all()
for registro in registros:
    print("Nome:", registro.atendente.nome)
    print("Quantidade de chamados:", registro.qtd_chamados)
    print("Quantidade registrada:", registro.qtd_registrados)
    print("Positivos:", registro.positivos)
    print("Negativos:", registro.negativos)
    print("Data:", registro.data)
    print()

# Deletar Analista e Atendimentos
# analista = Atendente.objects.filter(nome='Larissa')
#
# Atendimento.objects.filter(atendente__in=analista).delete()
#
# analista.delete()