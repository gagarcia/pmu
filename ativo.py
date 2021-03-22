class Ativo(object):
    """docstring for ativo."""

    def __init__(self, ticker):
        # self.resumo = {
        #     "nome": nome,
        #     "ticker": ticker,
        #     "quantidade": quantidade,
        #     "preco_medio": preco_medio,
        #     "tipo": tipo
        # }
        self.ticker = ticker

    def cadastra(self, user_id, tipo, quantidade, preco_medio):
        import psycopg2

        ticker = "'" + self.ticker + "'"
        tipo = "'" + tipo + "'"

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = "INSERT INTO carteiras(user_id,ticker,tipo,quantidade,preco_medio)values({},{},{},{},{})".format(user_id,ticker,tipo,quantidade,preco_medio)
        cur.execute(query)
        conn.commit()

        self.atualiza(user_id,quantidade,preco_medio, "compra")

        print("Eba! ativo cadastrado com sucesso!")

    def carrega(self,user_id):
        import psycopg2

        ticker = "'" + self.ticker + "'"

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = "SELECT * FROM carteiras WHERE user_id = {} AND ticker = {}".format(user_id,ticker)
        cur.execute(query)
        rows = cur.fetchall()

        self.resumo = {
            "userid": user_id,
            "ticker": rows[0][1],
            "tipo": rows[0][2],
            "quantidade": rows[0][3],
            "preco medio": rows[0][4]
        }

    def atualiza(self, user_id, qde_comprada, preco_medio_compra, tipo):
        import psycopg2

        self.carrega(user_id)
        ticker = "'" + self.ticker + "'"

        if tipo == "compra":
            quant_final = self.resumo["quantidade"] + qde_comprada
        else:
            quant_final = self.resumo["quantidade"] - qde_comprada

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = "UPDATE carteiras SET quantidade = {} WHERE user_id = {} AND ticker = {}".format(quant_final,user_id,ticker)
        cur.execute(query)
        conn.commit()


        if tipo == "compra":
            preco_medio = (self.resumo["preco medio"]*self.resumo["quantidade"] + preco_medio_compra*qde_comprada)/quant_final

            query = "UPDATE carteiras SET preco_medio = {} WHERE user_id = {} AND ticker = {}".format(preco_medio,user_id,ticker)
            cur.execute(query)
            conn.commit()

        self.atualiza_trans(user_id,qde_comprada,preco_medio_compra, tipo)

    def atualiza_trans(self,user_id,quantidade, preco_medio, tipo):
        import psycopg2
        ticker = "'" + self.ticker + "'"
        tipo = "'" + tipo + "'"

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = "INSERT INTO transacoes(ticker, quantidade, trans_time, user_id, preco_medio) values({}, {}, CURRENT_TIMESTAMP, {}, {})".format(ticker,quantidade, user_id, preco_medio)
        cur.execute(query)
        conn.commit()
