from abc import ABC, abstractmethod
from datetime import datetime

class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

    def realizar_transacao(self, conta, transacao):
        transacao.registrar(conta)

    def adicionar_conta(self, conta):
        self.contas.append(conta)


class PessoaFisica(Cliente):
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(endereco)
        self.nome = nome
        self.data_nascimento = data_nascimento
        self.cpf = cpf


class Conta:
    def __init__(self, numero, cliente):
        self._saldo = 0
        self._numero = numero
        self._agencia = "0001"
        self._cliente = cliente
        self._historico = Historico()

    @classmethod
    def nova_conta(cls, cliente, numero):
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @property
    def numero(self):
        return self._numero

    @property
    def agencia(self):
        return self._agencia

    @property
    def cliente(self):
        return self._cliente

    @property
    def historico(self):
        return self._historico

    def sacar(self, valor):
        saldo = self.saldo
        excedeu_saldo = valor > saldo

        if excedeu_saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")

        elif valor > 0:
            self._saldo -= valor
            print("\n=== Saque realizado com sucesso! ===")
            return True

        else:
            print("\nOperação falhou! O valor informado é inválido.")

        return False

    def depositar(self, valor):
        if valor > 0:
            self._saldo += valor
            print("\nDepósito realizado com sucesso!")
        else:
            print("\nOperação falhou! O valor informado é inválido.")
            return False

        return True


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        numero_saques = len(
            [transacao for transacao in self.historico.transacoes if transacao["tipo"] == Saque.__name__]
        )

        excedeu_limite = valor > self.limite
        excedeu_saques = numero_saques >= self.limite_saques

        if excedeu_limite:
            print("\nOperação falhou! O valor do saque excede o limite.")

        elif excedeu_saques:
            print("\nOperação falhou! Número máximo de saques excedido.")

        else:
            return super().sacar(valor)

        return False


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(
            {
                "tipo": transacao.__class__.__name__,
                "valor": transacao.valor,
                "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S"),
            }
        )


class Transacao(ABC):
    @property
    @abstractmethod
    def valor(self):
        pass

    @classmethod
    @abstractmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.sacar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        sucesso_transacao = conta.depositar(self.valor)

        if sucesso_transacao:
            conta.historico.adicionar_transacao(self)

def menu():
    menu = """
    Menu:

    1 - Depositar
    2 - Sacar
    3 - Extrato
    4 - Registrar cliente
    5 - Criar conta
    6 - Listar contas
    7 - Sair
    => """

    print(menu)


def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    if numero_saques < limite_saques:
        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite

        if excedeu_saldo:
            print("\nSaldo suficiente.")

        elif excedeu_limite:
            print("\nValor do saque excede o limite.")

        elif valor > 0:
            saldo -= valor
            extrato += f"Saque: R$ {valor:.2f}\n"
            numero_saques += 1
            print("\nSaque efetuado.\n")

        else:
            print("\nValor inválido.\n")
    
    else:
        print("\nLimite de saques excedido.")

    return saldo, extrato


def exibir_extrato(conta):
    print("\n================ EXTRATO ================")
    if conta.historico.transacoes:
        for transacao in conta.historico.transacoes:
            linha = f"""
            -----------------------------------------
            {transacao['tipo']}: {transacao['valor']}
            Data: {transacao['data']}
            -----------------------------------------
            """
            print(linha)
    else:
        print("\nSem movimentações.\n")

    print(f"\nSaldo:\t\tR$ {conta.saldo:.2f}")
    print("==========================================")


def filtrar_cliente(cpf, clientes):
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None

def filtrar_conta(numero, contas):
    contas_filtradas = [conta for conta in contas if conta.numero == numero]
    return contas_filtradas[0] if contas_filtradas else None


def criar_cliente(clientes):
    cpf = input("Informe o CPF (somente número): ")
    cliente = filtrar_cliente(cpf, clientes)

    if cliente:
        print("\nJá existe um cliente com esse CPF.\n")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, nro - bairro - cidade/sigla estado): ")

    novo_cliente = PessoaFisica(nome, data_nascimento, cpf, endereco)

    clientes.append(novo_cliente)

    print("Cliente registrado.\n")


def criar_conta(clientes, contas):
    cpf = input("Informe o CPF do cliente: ")
    cliente = filtrar_cliente(cpf, clientes)

    if not cliente:
        print("\nCliente não existe.\n")
        return
    
    nova_conta = ContaCorrente.nova_conta(cliente, len(contas) + 1)
    contas.append(nova_conta)
    cliente.contas.append(nova_conta)

    print("\nConta criada.\n")


def listar_contas(contas):
    for conta in contas:
        linha = f"""
        -----------------------------------------
        Agência: {conta.agencia}
        C/C: {conta.numero}
        Titular: {conta.cliente.nome}
        -----------------------------------------
        """
        print(linha)


def main():
    clientes = []
    contas = []

    opcao = 0

    while opcao != 7:
        menu()
        opcao = int(input())

        if opcao == 1:
            cpf_cliente = input("Informe seu CPF: ")

            cliente = filtrar_cliente(cpf_cliente, clientes)

            if cliente:
                num_conta = int(input("Informe o número da conta: "))
                conta = filtrar_conta(num_conta, cliente.contas)

                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    transacao = Deposito(valor)

                    cliente.realizar_transacao(conta, transacao)
                else:
                    print("Conta inexistente.\n")
            else:
                print("Cliente não existe.")

        elif opcao == 2:
            cpf_cliente = input("Informe seu CPF: ")

            cliente = filtrar_cliente(cpf_cliente, clientes)

            if cliente:
                num_conta = int(input("Informe o número da conta: "))
                conta = filtrar_conta(num_conta, cliente.contas)

                if conta:
                    valor = float(input("Informe o valor do depósito: "))
                    transacao = Saque(valor)

                    cliente.realizar_transacao(conta, transacao)
                else:
                    print("Conta inexistente.\n")
            else:
                print("Cliente não existe.\n")

        elif opcao == 3:
            cpf_cliente = input("Informe seu CPF: ")

            cliente = filtrar_cliente(cpf_cliente, clientes)

            if cliente:
                num_conta = int(input("Informe o número da conta: "))
                conta = filtrar_conta(num_conta, cliente.contas)

                if conta:
                    exibir_extrato(conta)
                else:
                    print("Conta inexistente.\n")
            else:
                print("Cliente não existe.\n")

        elif opcao == 4:
            criar_cliente(clientes)

        elif opcao == 5:
            criar_conta(clientes=clientes, contas=contas)

        elif opcao == 6:
            listar_contas(contas)

        elif opcao != 7:
            print("Operação inválida.")


main()
