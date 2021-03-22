from ativo import Ativo
from carteira import Carteira
import csv

ativos = []

# Importa os ativos da carteira de um CSV
with open('carteira_marco_2021 - Completa.csv') as csv_file:
    cart = csv.reader(csv_file, delimiter=';')

    for line in cart:
        # print(line[1])
        nome = line[0]
        ticker  = line[1]
        quantidade = line[3]
        preco_medio = line[4]
        tipo = line[5]
        ativos.append(Ativo(nome,ticker,quantidade,preco_medio,tipo))

#retira o header
ativos.pop(0)

from datetime import date


#datas da analise
start = '2017-01-01'
# end = str(date.today())
end = '2021-03-05'
#criação da carteira analisada
minha_carteira = Carteira(ativos,start,end)

print(minha_carteira.resuminho())
