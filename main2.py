from ativo import Ativo

# ticker = "24.582.422/0001-80"
ticker = input("ticker: ")
user_id = 8
tipo_transacao = ""
resposta = ""

ativo = Ativo(ticker)

try:
    ativo.carrega(user_id)
except:
    print("ativo não cadastrado!")
    resposta = input("deseja cadastrar?")

    if resposta == "y":
        tipo_transacao = "cadastro"
        qde_transacao = float(input('qde: '))
        preco_medio = float(input('preco medio de compra: '))
        tipo = input("tipo: ")
        ativo.cadastra(user_id,tipo,qde_transacao,preco_medio)
    elif("n"):
        print("Blz!")
        ticker = input("então digita ae um novo ticker: ")

print(ativo.resumo)

if tipo_transacao != "cadastro":
    tipo_transacao = input('tipo de transacao: ')
else:
    pass

qde_transacao = float(input('qde: '))

if tipo_transacao == "compra":
    preco_medio = float(input('preco medio de compra: '))
    ativo.atualiza(user_id,qde_transacao, preco_medio, "compra")
elif("venda"):
    ativo.atualiza(user_id,qde_transacao,0 , "venda")

ativo.carrega(user_id)

print(ativo.resumo)
