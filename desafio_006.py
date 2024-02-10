from abc import ABC, abstractclassmethod, abstractproperty
from datetime import datetime


class Cliente:
    def __init__(self, endereco):
        self.endereco = endereco
        self.contas = []

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
        if isinstance(cliente, Cliente):
            return cls(numero, cliente)
        else:
            raise ValueError("Cliente inválido.")

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
        if valor > self.saldo:
            print("Operação falhou! Saldo insuficiente.")
            return False
        elif valor <= 0:
            print("Operação falhou! Valor de saque inválido.")
            return False

        self._saldo -= valor
        print("Saque realizado com sucesso!")
        return True

    def depositar(self, valor):
        if valor <= 0:
            print("Operação falhou! Valor de depósito inválido.")
            return False

        self._saldo += valor
        print("Depósito realizado com sucesso!")
        return True

    def __str__(self):
        return f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
        """


class ContaCorrente(Conta):
    def __init__(self, numero, cliente, limite=500, limite_saques=3):
        super().__init__(numero, cliente)
        self.limite = limite
        self.limite_saques = limite_saques

    def sacar(self, valor):
        if valor > self.limite:
            print("Operação falhou! O valor do saque excede o limite.")
            return False
        elif len(self.historico.transacoes) >= self.limite_saques:
            print("Operação falhou! Número máximo de saques excedido.")
            return False

        return super().sacar(valor)


class Historico:
    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append({
            "tipo": transacao.__class__.__name__,
            "valor": transacao.valor,
            "data": datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        })


class Transacao(ABC):
    @property
    @abstractproperty
    def valor(self):
        pass

    @abstractclassmethod
    def registrar(self, conta):
        pass


class Saque(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.sacar(self.valor):
            conta.historico.adicionar_transacao(self)


class Deposito(Transacao):
    def __init__(self, valor):
        self._valor = valor

    @property
    def valor(self):
        return self._valor

    def registrar(self, conta):
        if conta.depositar(self.valor):
            conta.historico.adicionar_transacao(self)


# Exemplo de uso:
if __name__ == "__main__":
    # Criar cliente
    cliente = PessoaFisica("Fulano", "01-01-1990", "123.456.789-00", "Endereço")

    # Criar conta corrente
    conta_corrente = ContaCorrente.nova_conta(cliente, "123456")

    # Realizar transações
    saque = Saque(100)
    saque.registrar(conta_corrente)

    deposito = Deposito(500)
    deposito.registrar(conta_corrente)

    # Exibir saldo e histórico
    print(f"Saldo: {conta_corrente.saldo}")
    print("Histórico:")
    for transacao in conta_corrente.historico.transacoes:
        print(transacao)
