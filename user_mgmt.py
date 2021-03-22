class Usuario(object):
    """docstring for usuario."""

    def __init__(self,username):
        self.username = username

    def cadastro(self,nome,sobrenome,email,password):
        import psycopg2

        nome = "'" + nome + "'"
        sobrenome = "'" + sobrenome + "'"
        username = "'" + self.username + "'"
        email = "'" + email + "'"
        senha = "'" + password + "'"

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = "INSERT INTO account(nome,sobrenome,username,email,password,created_on)values({nominho},{sobrenome},{username},{email},{senha},CURRENT_TIMESTAMP)".format(nominho = nome,sobrenome=sobrenome,username=username,email=email,senha=senha)
        cur.execute(query)
        conn.commit()

        print("Eba! Usuarix cadastrado com sucesso!")

    def remove(self):
        import psycopg2

        conn = psycopg2.connect(
            database  = "finance",
            user = "postgres",
            password = "PASSWORD",
            port = "5432"
        )

        cur = conn.cursor()

        query = ("")
        cur.execute(query)
        conn.commit()

    def loga(self):
        try:
            usuario_mod = "'" + self.username + "'"
            query = "SELECT * FROM account WHERE username = " + usuario_mod

            import psycopg2

            conn = psycopg2.connect(
                database  = "finance",
                user = "postgres",
                password = "PASSWORD",
                port = "5432"
            )

            cur = conn.cursor()
            cur.execute(query)
            rows = cur.fetchall()

            self.resumo = {
                "userid": rows[0][0],
                "usuario": self.username,
                "nome": rows[0][2],
                "sobrenome": rows[0][3],
                "password": rows[0][4],
                "email": rows[0][5]
            }


        except:
            print("Usuário não encontrado")
