menu = """
-----------------------

1 - Depositar
2 - Sacar
3 - Consultar extrato
4 - Sair

-----------------------

O que deseja fazer: 
"""
opcao = 0

saldo = 0
limite = 500
extrato = ""
num_saques = 0
LIMITE_SAQUE = 3

while opcao != 4:
    opcao = int(input(menu))

    if opcao == 1:
        valor = float(input("Informe o valor a ser depositado: "))

        if valor > 0:
            saldo += valor
            extrato += f"Depósito: R$ {valor:.2f}\n"
        else:
            print("Valor inválido.\n")

    elif opcao == 2:
        if num_saques < LIMITE_SAQUE:
            valor = float(input("Digite o valor a ser sacado: "))

            excedeu_saldo = valor > saldo
            excedeu_limite = valor > limite
            
            if excedeu_limite:
                print("Valor do saque excedido.\n")
            elif excedeu_saldo:
                print("Saldo insuficiente.\n")
            else:
                saldo -= valor
                extrato += f"Saque: {valor:.2f}\n"
                num_saques += 1
            
        else:
            print("Limite de saques excedido.\n")

    elif opcao == 3:
        print("--------------Extrato--------------\n")
        print("Não foram realizadas movimentações." if not extrato else extrato)
        print(f"\nSaldo: R$ {saldo:.2f}\n")
        print("-----------------------------------\n")

    elif opcao != 4:
        print("Operação inválida.\n")
