import json
import datetime

menu = """
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

dados = {}
dados = json.dumps(dados)
with open("dados.json", "r") as f:
    dados = f.read()
    f.close
dados = json.loads(dados)

mes = datetime.date.today().strftime("%B")
if mes == "January":
    mes = "Janeiro"
elif mes == "February":
    mes = "Fevereiro"
elif mes == "March":
    mes = "Março"
elif mes == "April":
    mes = "Abril"
elif mes == "May":
    mes = "Maio"
elif mes == "June":
    mes = "Junho"
elif mes == "July":
    mes = "Julho"
elif mes == "August":
    mes = "Agosto"
elif mes == "September":
    mes = "Setembro"
elif mes == "October":
    mes = "Outubro"
elif mes == "November":
    mes = "Novembro"
else:
    mes = "Dezembro"

if mes != dados["mes"]:
    dados["mes"] = mes
    dados["extrato"] = f"Saldo anterior: R$ {dados["saldo"]:.2f}\n\n"
    dados = json.dumps(dados)
    with open("dados.json", "w") as f:
        f.write(dados)
        f.close
    dados = json.loads(dados)

if datetime.date.today().strftime("%d/%m/%Y") != dados["data"]:
    dados["data"] = datetime.date.today().strftime("%d/%m/%Y")
    dados["saques"] = 0
    dados = json.dumps(dados)
    with open("dados.json", "w") as f:
        f.write(dados)
        f.close
    dados = json.loads(dados)

def salva_dados():
    global dados
    dados = json.dumps(dados)
    with open("dados.json", "w") as f:
        f.write(dados)
        f.close
    dados = json.loads(dados)

while True:

    opcao = input(menu)

    if opcao == "d":
        try:
            valor = float(input("Digite o valor do depósito: "))
        except ValueError:
            print("Valor inválido")
            continue
        dados["saldo"] += valor
        dados["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        salva_dados()

    elif opcao == "s":
        if dados["saques"] >= dados["LIMITE_SAQUES"]:
            print("Limite de saques excedido")
            continue
        try:
            valor = float(input("Digite o valor do saque: "))
        except ValueError:
            print("Valor inválido")
            continue
        if valor > dados["limite"] or valor > dados["saldo"]:
            print("Operação não permitida")
        else:
            dados["saldo"] -= valor
            dados["extrato"] += f"Saque: R$ {valor:.2f}\n"
            dados["saques"] += 1
            salva_dados()

    elif opcao == "e":
        print(f"\n==========Extrato {mes}==========")
        print(dados["extrato"])
        print(f"\nSaldo: R$ {dados["saldo"]:.2f}")
        print("=================================")

    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")