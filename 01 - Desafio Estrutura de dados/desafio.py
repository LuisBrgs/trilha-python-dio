import json
import datetime
import textwrap
import random

dados = {}
dados = json.dumps(dados)
with open("dados.json", "r") as f:
    dados = f.read()
    f.close
dados = json.loads(dados)

def salva_dados(dados):
    dados = json.dumps(dados)
    with open("dados.json", "w") as f:
        f.write(dados)
        f.close
    dados = json.loads(dados)

def validacao_cpf(cpf):
    try:
        cpf = str(cpf)
        if len(cpf) != 11:
            return False
        if cpf == cpf[::-1]:
            return False
        value = 0
        for i in range(9):
            value += int(cpf[i]) * (10-i)
        digit = (value * 10) % 11
        if digit >= 10:
            digit = 0
        if digit != int(cpf[9]):
            return False
        value = 0
        for i in range(10):
            value += int(cpf[i]) * (11-i)
        digit = (value * 10) % 11
        if digit >= 10:
            digit = 0
        if digit != int(cpf[10]):
            return False    
        return True
    except:
        return False

def novo_usuario(dados, cpf):
    senha = input("Usuário não cadastrado,\nVamos criar seu acesso e sua primeira conta!\n\nCrie uma senha para seu CPF: ")
    nome = input("Informe seu nome completo: ")
    email = input("Email: ")
    endereco = input("Endereço: ")
    dados.update({cpf: {"senha": senha, "nome": nome, "email": email, "endereco": endereco, "contas": {}}})
    salva_dados(dados)
    print("\nAgora vamos criar sua primeira conta!\n")
    nova_conta(dados, cpf)
    salva_dados(dados)

def nova_conta(dados, cpf):
    while True:
        nome_conta = input("\nDê um nome para sua nova conta ou digite 'v' para voltar: ")
        if nome_conta in dados[cpf]["contas"]:
            print("Você já possui uma conta com este nome, tente outro.\n")
            continue
        elif nome_conta == "v":
            if dados[cpf]["contas"] == {}:
                print("Precisa criar ao menos uma conta para iniciar as operações.\n")
            continue
        elif len(nome_conta) < 3:
            print("O nome de sua conta precisa conter ao menos 3 caracteres, tente novamente.\n")
            continue
        else:
            dados[cpf]["contas"].update({nome_conta: {"agencia": 100, "numero_conta": 0, "saques": 0, "saldo": 0, "limite": 500, "extrato": "", "LIMITE_SAQUES": 3}})
            num_conta = random.randint(1, 100000)
            while True:
                for i in dados.keys():
                    try:
                        for j in dados[i]["contas"].keys():
                            if num_conta == dados[i]["contas"][j]["numero_conta"]:
                                num_conta = random.randint(10000, 99999)
                                continue
                    except:
                        continue
                break
            dados[cpf]["contas"][nome_conta]["numero_conta"] = num_conta
            print("Conta criada com sucesso!\n")
            salva_dados(dados)
            break

def login(dados):
    while True:
        cpf = input("LOGIN\n\nCPF: ")
        if cpf in dados.keys():
            senha = input("Senha: ")
            if senha == dados[cpf]["senha"]:
                print("LogIn realizado com sucesso!")
            else:
                print("Senha inválida.")
                continue
        else:
            if validacao_cpf(cpf):
                novo_usuario(dados, cpf)
            else:
                print("CPF inválido! Digite apenas números.\n")
                continue
        break
    return cpf

def listar_contas(dados, cpf):
    if dados[cpf]["contas"] == {}:
        print("Vamos criar sua primeira conta:\n")
        nova_conta(dados, cpf)
    while True:
        n=0
        print("=============== CONTAS ===============")
        for i in dados[cpf]["contas"].keys():
            n+=1
            print(f'[{n}]: {i}')
        try:
            conta = input('\nSelecione a conta na qual gostaria de operar: ')
            conta = list(dados[cpf]["contas"].keys())[int(conta)-1]
        except:
            print('Digite apenas o número correspondente à conta conforme indicado.\n')
            continue
        break
    return conta

def menu():
    menu = """\n
    ================ MENU ================
    [d]\tDepositar
    [s]\tSacar
    [e]\tExtrato
    [nc]\tNova conta
    [lc]\tListar contas
    [a]\tAlterar dados de usuário
    [dc]\tConsulta dados da conta
    [q]\tSair
    => """
    return input(textwrap.dedent(menu))

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
    for cpf in dados:
        try:
            for contas in dados[cpf]:
                for nome in dados[cpf][contas]:
                    if "extrato" in dados[cpf][contas][nome]:
                        dados[cpf][contas][nome]["extrato"] = f"Saldo anterior: R$ {dados[cpf][contas][nome]["saldo"]:.2f}\n\n"
                        dados = json.dumps(dados)
        except:
            continue
    salva_dados(dados)

if datetime.date.today().strftime("%d/%m/%Y") != dados["data"]:
    dados["data"] = datetime.date.today().strftime("%d/%m/%Y")
    for cpf in dados:
        try:
            for contas in dados[cpf]:
                for nome in dados[cpf][contas]:
                    if "saques" in dados[cpf][contas][nome]:
                        dados[cpf][contas][nome]["saques"] = 0
        except:
            continue
    salva_dados(dados)

cpf = login(dados)
conta = listar_contas(dados, cpf)


while True:

    opcao = menu()

    if opcao == "d":
        try:
            valor = float(input("Digite o valor do depósito: "))
        except ValueError:
            print("Valor inválido")
            continue
        dados[cpf]["contas"][conta]["saldo"] += valor
        dados[cpf]["contas"][conta]["extrato"] += f"Depósito: R$ {valor:.2f}\n"
        salva_dados(dados)

    elif opcao == "s":
        if dados[cpf]["contas"][conta]["saques"] >= dados[cpf]["contas"][conta]["LIMITE_SAQUES"]:
            print("Limite de saques excedido")
            continue
        try:
            valor = float(input("Digite o valor do saque: "))
        except ValueError:
            print("Valor inválido")
            continue
        if valor > dados[cpf]["contas"][conta]["limite"] or valor > dados[cpf]["contas"][conta]["saldo"]:
            print("Operação não permitida")
        else:
            dados[cpf]["contas"][conta]["saldo"] -= valor
            dados[cpf]["contas"][conta]["extrato"] += f"Saque: R$ {valor:.2f}\n"
            dados[cpf]["contas"][conta]["saques"] += 1
            salva_dados(dados)

    elif opcao == "e":
        print(f"\n==========Extrato {mes}==========")
        print(dados[cpf]["contas"][conta]["extrato"])
        print(f"\nSaldo: R$ {dados[cpf]["contas"][conta]["saldo"]:.2f}")
        print("=================================")

    elif opcao == "nc":
        nova_conta(dados, cpf)
        conta = listar_contas(dados, cpf)

    elif opcao == "lc":
        conta = listar_contas(dados, cpf)

    elif opcao == "a":
        senha = input("\nConfirme com sua senha: ")
        if senha != dados[cpf]["senha"]:
            print("Senha incorreta.")
            continue
        else:
            print(f"""\n
    Qual dado gostaria de alterar?
                  
    [1]\tNome: {dados[cpf]["nome"]}
    [2]\tSenha: {dados[cpf]["senha"]}
    [3]\tE-mail: {dados[cpf]["email"]}
    [4]\tEndereço: {dados[cpf]["endereco"]}""")
            opcao2 = input()
            if opcao2 == "1":
                dados[cpf]["nome"] = input("Digite o nome correto: ")
            elif opcao2 == "2":
                dados[cpf]["senha"] = input("Digite a nova senha: ")
            elif opcao2 == "3":
                dados[cpf]["email"] = input("Digite o email correto: ")
            elif opcao2 == "4":
                dados[cpf]["endereco"] = input("Digite o novo endereço: ")
            else:
                print("Opção inválida.")

    elif opcao == "dc":
        print(f'\nConta {conta}\nAgência: {dados[cpf]["contas"][conta]["agencia"]}\nNúmero da conta: {dados[cpf]["contas"][conta]["numero_conta"]}')
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")