class Carteira(object):
    """docstring for carteira."""

    def __init__(self, ativos, start, end):

        self.empresas = []
        self.tickers = []
        self.quantidades = []
        self.precos_medios = []
        self.tipos = []
        self.start = start
        self.end = end

        for ativo in ativos:
            self.empresas.append(ativo.resumo['nome'])
            self.tickers.append(ativo.resumo['ticker'])
            self.quantidades.append(float(ativo.resumo['quantidade']))
            self.precos_medios.append(float(ativo.resumo['preco_medio']))
            self.tipos.append(ativo.resumo['tipo'])

        def historico_precos():
            import pandas as pd
            import pandas_datareader as wb
            import re
            import numpy as np

            start = self.start
            end = self.end

            precos = pd.DataFrame()
            i = 0

            for t in self.tickers:
                tipo = self.tipos[i]

                if tipo == "acao":
                    precos[t] = wb.DataReader(t,'yahoo',start=start,end=end)['Adj Close']

                else:
                    print("ativo: {}" .format(t))
                    nome_arq = re.sub('[./-]', '', t)
                    fundos = pd.read_csv('fundos_select/'+nome_arq+'.csv')
                    fundos['DT_COMPTC'] = pd.to_datetime(fundos['DT_COMPTC'],format = '%Y-%m-%d')
                    fundos.set_index('DT_COMPTC',inplace = True)
                    # print(fundos)
                    # precos[t] = np.nan
                    precos = precos.merge(fundos, left_index=True, right_index=True, how='left')

                i = i + 1
                print(precos)
            return precos

        self.precos = historico_precos()

    def sharpe(self):
        import pandas as pd
        import numpy as np

        pesos = np.multiply(self.quantidades,self.precos_medios)/np.dot(self.quantidades,self.precos_medios)

        prices = self.precos

        prices_norm = prices/prices.iloc[0]

        alloc = pd.DataFrame(columns=prices_norm.columns, index=prices_norm.index)

        for (column, peso) in zip(prices_norm.columns, pesos):
            alloc[column] = prices_norm[column].apply(lambda x: x*peso)

        alloc['total'] = alloc.sum(axis=1)

        alloc['retorno diario'] = alloc['total'].pct_change(1)

        sharpe = (alloc['retorno diario'].mean()*(252**0.5))/alloc['retorno diario'].std()

        dados = {
            "sharpe": sharpe,
            "valorizacao": alloc["total"].iloc[-1],
            "retorno_diario_medio": alloc['retorno diario'].mean(),
            "volatilidade": alloc['retorno diario'].std()
        }

        return dados

    def grafico(self):
        import matplotlib.pyplot as plt

        prices = self.precos

        plt.figure()

        (prices/prices.iloc[0]).plot(figsize=(20,10))
        (prices/prices.iloc[0]).rolling(21).mean().plot(figsize=(20,10))

        plt.show()


    def opt(self):

        def calc_ret_vol_sr(weights):
            weights = np.array(weights)
            ret = np.sum(log_ret.mean() * weights) * 252
            vol = np.sqrt(np.dot(weights.T,np.dot(log_ret.cov()*252,weights)))
            sr = ret/vol
            return np.array([ret,vol,sr])

        def neg_sharpe(weights):
            return calc_ret_vol_sr(weights)[2] * -1

        def check_soma(weights):
            #retorna 0 se a somas dos pesos totalizam 1
            return np.sum(weights) - 1

        cons = ({'type':'eq',
                'fun':check_soma})

    def resuminho(self):
        sharpe = self.sharpe()
        patrimonio = pass

        resumo = {
            "empresas": self.empresas,
            "sharpe": sharpe["sharpe"],
            "valorizacao": sharpe["valorizacao"],
            "volatilidade": sharpe["volatilidade"]*100
            "Patrimonio total":
        }

        return resumo

    def adiciona_ativo(self, nome, ticker, quantidade, preco_medio, tipo):
        from ativo import ativo

        ativo_add = Ativo(nome,ticker,quantidade,preco,preco_medio,tipo)

        self.empresas.append(ativo_add.resumo['nome'])
        self.tickers.append(ativo_add.resumo['ticker'])
        self.quantidades.append(float(ativo_add.resumo['quantidade']))
        self.precos_medios.append(float(ativo_add.resumo['preco_medio']))
