class Teste:
    def __init__(self, x):
        self.x = x

    def printar (self):
        return self.x, "oi"

    def __str__(self):
        return f"{self.x}"


Teste.printar(Teste(1))

a = Teste(5)
print(a.x)
c, d = a.printar()
print(d)


dados = {
    "data": "", 
    "mes": "", 
    "users": [
        {
            "CPF": "02547598723",
            "senha": "senha123",
            "nome": "João da Silva",
            "email": "joao@email.com",
            "endereco": "Rua Principal, 123",
            "contas": [{},
                {
                    "nome": "Corrente",
                    "numero_conta": "123456",
                    "agencia": 100,
                    "saques": 0,
                    "saldo": 0,
                    "limite": 500,
                    "extrato": "",
                    "LIMITE_SAQUES": 3
                }, {}, {}, {}
            ]
        }
    ]
}

for i in range(len(dados["users"])):
    for n in range(len(dados["users"][i]["contas"])):
        print(100 in dados["users"][i]["contas"][n].values())
        if 100 in dados["users"][i]["contas"][n].values():
            print("Achou no ", i, ", ", n)
            break

x = y = 10
print(x, y)