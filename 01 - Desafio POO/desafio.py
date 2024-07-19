import json
import datetime
import textwrap
import random

dados = {}
with open("dados.json", "r") as f:
    dados = json.load(f)
    f.close

def salva_dados(dados):
    with open("dados.json", "w") as f:
        json.dump(dados, f)
        f.close

def localiza_conta(usuario, nome_conta):
    posicao_conta = posicao_usuario = None
    for i in range(len(dados['users'])):
        if usuario.cpf in dados['users'][i].values():
            posicao_usuario = i
            for j in range(len(dados['users'][i]['contas'])):
                if nome_conta in dados['users'][i]['contas'][j].values():
                    posicao_conta = j
    return posicao_conta, posicao_usuario

class User:
    def __init__(self, cpf="", senha="", nome="", email="", endereco="", contas=[]):
        self.cpf = cpf
        self.senha = senha
        self.nome = nome
        self.email = email
        self.endereco = endereco
        self.contas = contas
    
    def novo_usuario(self, usuario, conta, dados, cpf):
        usuario.senha = input("Usuário não cadastrado,\nVamos criar seu acesso e sua primeira conta!\n\nCrie uma senha para seu CPF: ")
        usuario.nome = input("Informe seu nome completo: ")
        usuario.email = input("Email: ")
        usuario.endereco = input("Endereço: ")
        usuario.cpf = cpf
        dados["users"].append({"CPF": cpf, "senha": self.senha, "nome": self.nome, "email": self.email, "endereco": self.endereco, "contas": self.contas})
        salva_dados(dados)
        print("\nAgora vamos criar sua primeira conta!\n")
        conta = conta.nova_conta(usuario, dados)
        salva_dados(dados)

    def __str__(self) -> str:
        return f'CPF: {self.cpf}, Nome: {self.nome}, Email: {self.email}, Endereço: {self.endereco}, Contas: {self.contas}'

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

class Conta(User):
    def __init__(self, nome_conta="", agencia=100, num_conta=0, saques=0, saldo=0, limite=500, extrato="", LIMITE_SAQUES=3):
        self.nome_conta = nome_conta
        self.agencia = agencia
        self.num_conta = num_conta
        self.saques = saques
        self.saldo = saldo
        self.limite = limite
        self.extrato = extrato
        self.LIMITE_SAQUES = LIMITE_SAQUES

    def nova_conta(self, usuario, dados):
        while True:
            nome_conta = input("\nDê um nome para sua nova conta ou digite 'v' para voltar: ")
            posicao_conta, posicao_usuario = localiza_conta(usuario, nome_conta)
            for i in range(len(dados["users"][posicao_usuario]["contas"])):
                if nome_conta in dados["users"][posicao_usuario]["contas"][i].values():
                    print("Você já possui uma conta com este nome, tente outro.\n")
                    continue
            if nome_conta == "v":
                if dados["users"][posicao_usuario]["contas"] == []:
                    print("Precisa criar ao menos uma conta para iniciar as operações.\n")
                    continue
                else:
                    break
            elif len(nome_conta) < 3:
                print("O nome de sua conta precisa conter ao menos 3 caracteres, tente novamente.\n")
                continue
            else:
                num_conta = random.randint(10000, 99999)
                while True:
                    for i in range(len(dados['users'][posicao_usuario]['contas'])):
                        if num_conta in dados['users'][posicao_usuario]['contas'][i].values():
                            num_conta = random.randint(10000, 99999)
                            continue
                    break
                dados['users'][posicao_usuario]["contas"].append({"nome_conta": nome_conta, "agencia": 100, "num_conta": num_conta, "saques": 0, "saldo": 0, "limite": 500, "extrato": "", "LIMITE_SAQUES": 3})
                print("Conta criada com sucesso!\n")
                salva_dados(dados)
                break
            print("Erro de usuário não cadastrado, tente novamente\n")

    def sacar(self, usuario, conta, dados):
        posicao_conta, posicao_usuario = localiza_conta(usuario, conta.nome_conta)
        while True:
            if dados['users'][posicao_usuario]["contas"][posicao_conta]["saques"] >= dados['users'][posicao_conta]["contas"][posicao_usuario]["LIMITE_SAQUES"]:
                print("Limite de saques excedido")
                break
            try:
                valor = float(input("Digite o valor do saque: "))
            except ValueError:
                print("Valor inválido")
                break
            if valor <= 0:
                print("Valor inválido")
                break
            elif valor > dados['users'][posicao_usuario]["contas"][posicao_conta]["limite"]:
                print(f"Seu limite para essa transação é de R$ {dados['users'][posicao_usuario]["contas"][posicao_conta]["limite"]:.2f}")
            elif valor > dados['users'][posicao_usuario]["contas"][posicao_conta]["saldo"]:
                print("Saldo insuficiente.")
            else:
                dados['users'][posicao_usuario]["contas"][posicao_conta]["saldo"] -= valor
                dados['users'][posicao_usuario]["contas"][posicao_conta]["extrato"] += f"Saque: R$ {valor:.2f}\n"
                dados['users'][posicao_usuario]["contas"][posicao_conta]["saques"] += 1
                salva_dados(dados)
                conta.saldo = dados['users'][posicao_usuario]["contas"][posicao_conta]["saldo"]
                conta.extrato = dados['users'][posicao_usuario]["contas"][posicao_conta]["extrato"]
                conta. saques = dados['users'][posicao_usuario]["contas"][posicao_conta]["saques"]
                break

    def depositar(self, usuario, conta, dados):
        posicao_conta, posicao_usuario = localiza_conta(usuario, conta.nome_conta)
        while True:
            try:
                valor = float(input("Digite o valor do depósito: "))
            except ValueError:
                print("Valor inválido")
                break
            if valor <= 0:
                print("Valor inválido")
                break
            else:
                dados['users'][posicao_usuario]["contas"][posicao_conta]["saldo"] += valor
                dados['users'][posicao_usuario]["contas"][posicao_conta]["extrato"] += f"Depósito: R$ {valor:.2f}\n"
                salva_dados(dados)
                conta.saldo = dados['users'][posicao_usuario]["contas"][posicao_conta]["saldo"]
                conta.extrato = dados['users'][posicao_usuario]["contas"][posicao_conta]["extrato"]
                print("Depósito realizado com sucesso!\n")
                break

    def listar_contas(self, usuario, dados):
        posicao_conta, posicao_usuario = localiza_conta(usuario, "")
        if usuario.cpf in dados['users'][posicao_usuario].values() and dados['users'][posicao_usuario]['contas'] == []:
            print("Vamos criar sua primeira conta:\n")
            User.nova_conta(usuario, dados)
            conta = Conta(dados['users'][posicao_usuario]['contas'][0]['nome_conta'], 100, dados['users'][posicao_usuario]['contas'][0]['num_conta'], 0, 0, 500, "", 3)
        while True:
            n=0
            print("=============== CONTAS ===============")
            for i in range(len(dados['users'][posicao_usuario]['contas'])):
                n+=1
                print(f'[{n}]: {dados['users'][posicao_usuario]['contas'][i]['nome_conta']}')
            try:
                conta = int(input('\nSelecione a conta na qual gostaria de operar: '))
                if conta <= 0:
                    raise ValueError
                conta = Conta(dados['users'][posicao_usuario]["contas"][int(conta)-1]['nome_conta'], 100, dados['users'][posicao_usuario]["contas"][int(conta)-1]["num_conta"], dados['users'][posicao_usuario]["contas"][int(conta)-1]["saques"], dados['users'][posicao_usuario]["contas"][int(conta)-1]["saldo"], dados['users'][posicao_usuario]["contas"][int(conta)-1]["limite"], dados['users'][posicao_usuario]["contas"][int(conta)-1]["extrato"], dados['users'][posicao_usuario]["contas"][int(conta)-1]["LIMITE_SAQUES"])
            except:
                print('Digite apenas o número correspondente à conta conforme indicado.\n')
                continue
            break
        return conta
    
    def __str__(self):
        return f'Agência: {self.agencia}, Número da conta: {self.num_conta}, Saques: {self.saques}, Saldo: {self.saldo}, Limite: {self.limite}, Extrato: {self.extrato}, Limite de saques: {self.LIMITE_SAQUES}'

def login(usuario, conta, dados):
    while True:
        cpf = input("LOGIN\n\nCPF: ")
        for i in range(len(dados['users'])):
            if cpf in dados['users'][i].values():
                senha = input("Senha: ")
                usuario = User(dados['users'][i]['CPF'], dados['users'][i]['senha'], dados['users'][i]['nome'], dados['users'][i]['email'], dados['users'][i]['endereco'], dados['users'][i]['contas'])
                if senha == dados['users'][i]["senha"]:
                    print("LogIn realizado com sucesso!")
                    break
                else:
                    print("Senha inválida.")
                    continue
        if cpf not in usuario.cpf:
            if validacao_cpf(cpf):
                usuario.novo_usuario(usuario, conta, dados, cpf)
            else:
                print("CPF inválido! Digite apenas números.\n")
                continue
        if cpf in usuario.cpf and senha in usuario.senha:
            break
    return usuario

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
    for i in range(len(dados['users'])):
        if dados['users'][i] != []:
            for n in range(len(dados['users'][i]['contas'])):
                dados['users'][i]['contas'][n]['extrato'] = f'Sando anterior: R$ {dados['users'][i]['contas'][n]['saldo']:.2f}\n\n'
                salva_dados(dados)

if datetime.date.today().strftime("%d/%m/%Y") != dados["data"]:
    dados["mes"] = mes
    for i in range(len(dados['users'])):
        if dados['users'][i] != []:
            for n in range(len(dados['users'][i]['contas'])):
                dados['users'][i]['contas'][n]['saques'] = 0
                salva_dados(dados)

usuario = User()
conta = Conta()
for i in range(len(dados['users'])):
    if usuario.cpf in dados['users'][i].values():
        cpf = usuario.cpf
usuario = login(usuario, conta, dados)
conta = conta.listar_contas(usuario, dados)
posicao_conta, posicao_usuario = localiza_conta(usuario, conta.nome_conta)


while True:

    opcao = menu()

    if opcao == "d":
        conta.depositar(usuario, conta, dados)

    elif opcao == "s":
        conta.sacar(usuario, conta, dados)

    elif opcao == "e":
        print(f"\n==========Extrato {mes}==========")
        print(conta.extrato)
        print(f"\nSaldo: R$ {conta.saldo:.2f}")
        print("=================================")

    elif opcao == "nc":
        conta.nova_conta(usuario, dados)
        conta = conta.listar_contas(usuario, dados)
        print("=================================")

    elif opcao == "lc":
        conta = conta.listar_contas(usuario, dados)

    elif opcao == "a":
        senha = input("\nConfirme com sua senha: ")
        if senha != usuario.senha:
            print("Senha incorreta.")
        else:
            print(f"""\n
    Qual dado gostaria de alterar?
                  
    [1]\tNome: {usuario.nome}
    [2]\tSenha: {usuario.senha}
    [3]\tE-mail: {usuario.email}
    [4]\tEndereço: {usuario.endereco}""")
            opcao2 = input()
            if opcao2 == "1":
                usuario.nome = dados["users"][posicao_usuario]["nome"] = input("Digite o nome correto: ")
            elif opcao2 == "2":
                usuario.senha = dados["users"][posicao_usuario]["senha"] = input("Digite a nova senha: ")
            elif opcao2 == "3":
                usuario.email = dados["users"][posicao_usuario]["email"] = input("Digite o email correto: ")
            elif opcao2 == "4":
                usuario.endereco = dados["users"][posicao_usuario]["endereco"] = input("Digite o novo endereço: ")
            else:
                print("Opção inválida.")

    elif opcao == "dc":
        print(f'\nConta {conta.nome_conta}\nAgência: {conta.agencia}\nNúmero da conta: {conta.num_conta}')
    
    elif opcao == "q":
        break

    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")
