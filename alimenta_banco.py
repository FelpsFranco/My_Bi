# import os
# import django
#
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')
# django.setup()

from Analisedados.models import Atendimento, Atendente



# atendente1 = Atendente.objects.create(nome='Victor')
# atendente1.save()
#
#
# registrados = [0, 0, 9, 7, 0, 16, 0, 0, 0, 0, 14, 4, 0, 7, 0, 0, 14, 0, 9, 7, 0, 0, 0, 18, 7, 0, 19, 7, 0, 0]
# chamados = [0, 0, 8, 6, 9, 9, 0, 0, 0, 12, 4, 3, 7, 6, 0, 0, 8, 8, 8, 5, 0, 0, 0, 10, 3, 7, 6, 7, 0, 0]
# qtd_positivos = [0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 1, 2, 0, 0, 0, 2, 0, 1, 0, 1, 0, 0]
# qtd_negativos = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
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



# # Mostrar todos
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

# nome_analista = "Davi"
# analista = Atendente.objects.get(nome=nome_analista)
#
# # Filtra os chamados pelo analista
# chamados = Atendimento.objects.filter(atendente=analista)
#
# # Exibe os chamados
# for chamado in chamados:
#     print(f"ID: {chamado.id}, Analista: {chamado.atendente}, Data: {chamado.data}")


# ids_chamados = [143]
# Atendimento.objects.filter(id__in=ids_chamados).delete()
