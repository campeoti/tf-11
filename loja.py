# Loja do TF 11 - passo 8: sem else e um nivel de indentacao por metodo.
# Rodar no terminal: python3 loja.py


# Cpf: so existe se tiver 11 caracteres, assim um cpf errado nao entra no sistema.
class Cpf:
    def __init__(self, numero):
        if len(numero) != 11:
            raise ValueError("cpf invalido")
        self.__numero = numero


# Email: nao aceita email vazio nem sem arroba.
class Email:
    def __init__(self, endereco):
        if len(endereco) == 0:
            raise ValueError("email vazio")
        if "@" not in endereco:
            raise ValueError("email invalido")
        self.__endereco = endereco


# Cep: so existe se tiver 8 caracteres.
class Cep:
    def __init__(self, numero):
        if len(numero) != 8:
            raise ValueError("cep invalido")
        self.__numero = numero


# Dinheiro: guarda o valor em centavos (int) e faz as contas sem erro de float.
class Dinheiro:
    def __init__(self, centavos):
        self.__centavos = centavos

    def somar(self, outro):
        return Dinheiro(self.__centavos + outro.__centavos)

    def subtrair(self, outro):
        return Dinheiro(self.__centavos - outro.__centavos)

    def multiplicar(self, quantidade):
        return Dinheiro(self.__centavos * quantidade)

    def percentual(self, porcentagem):
        return Dinheiro(self.__centavos * porcentagem // 100)

    def __str__(self):
        return "R$ %d.%02d" % (self.__centavos // 100, self.__centavos % 100)


# Status: guarda a letra do status do pedido e sabe se descrever.
class Status:
    __DESCRICOES = {"A": "aberto", "P": "pago", "C": "cancelado"}

    def __init__(self, codigo):
        self.__codigo = codigo

    def descrever(self):
        return self.__DESCRICOES[self.__codigo]

    def esta_aberto(self):
        return self.__codigo == "A"

    def esta_pago(self):
        return self.__codigo == "P"


# Pessoa: os dados que identificam alguem (nome, cpf e email).
class Pessoa:
    def __init__(self, nome, cpf, email):
        self.__nome = nome
        self.__cpf = cpf
        self.__email = email

    def descrever(self):
        return self.__nome


# Endereco: onde o cliente mora (rua, cidade e cep).
class Endereco:
    def __init__(self, rua, cidade, cep):
        self.__rua = rua
        self.__cidade = cidade
        self.__cep = cep

    def descrever(self):
        return self.__cidade


# TipoNormal: cliente comum, nao ganha desconto.
class TipoNormal:
    def desconto_sobre(self, valor):
        return Dinheiro(0)


# TipoVip: cliente vip, ganha 10% de desconto.
class TipoVip:
    def desconto_sobre(self, valor):
        return valor.percentual(10)


# TipoFuncionario: funcionario da loja, ganha 20% de desconto.
class TipoFuncionario:
    def desconto_sobre(self, valor):
        return valor.percentual(20)


# Cliente: junta a pessoa, o endereco e o tipo de cliente.
class Cliente:
    def __init__(self, pessoa, endereco, tipo):
        self.__pessoa = pessoa
        self.__endereco = endereco
        self.__tipo = tipo    # TipoNormal, TipoVip ou TipoFuncionario

    def descrever(self):
        nome = self.__pessoa.descrever()
        cidade = self.__endereco.descrever()
        return nome + " - " + cidade

    def calcular_desconto(self, valor):
        return self.__tipo.desconto_sobre(valor)


# Produto: o que a loja vende, com nome e preco.
class Produto:
    def __init__(self, nome, preco):
        self.__nome = nome
        self.__preco = preco

    def descrever(self):
        return self.__nome

    def calcular_preco(self, quantidade):
        return self.__preco.multiplicar(quantidade)


# ItemDoPedido: um produto dentro do pedido e a quantidade comprada dele.
class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.__produto = produto
        self.__quantidade = quantidade

    def calcular_subtotal(self):
        return self.__produto.calcular_preco(self.__quantidade)

    def imprimir(self):
        print("  ", self.__quantidade, "x", self.__produto.descrever(), "=", self.calcular_subtotal())


# ItensDoPedido: a lista de itens de um pedido, com as contas em cima dela.
class ItensDoPedido:
    def __init__(self):
        self.__itens = []

    def adicionar(self, item):
        self.__itens.append(item)

    def esta_vazia(self):
        return len(self.__itens) == 0

    def calcular_total(self):
        total = Dinheiro(0)
        for item in self.__itens:
            subtotal = item.calcular_subtotal()
            total = total.somar(subtotal)
        return total

    def imprimir(self):
        for item in self.__itens:
            item.imprimir()


# Pedido: a compra de um cliente; ele mesmo decide se pode ser pago ou cancelado.
class Pedido:
    def __init__(self, cliente):
        self.__cliente = cliente
        self.__itens = ItensDoPedido()
        self.__status = Status("A")

    def adicionar_item(self, produto, quantidade):
        self.__itens.adicionar(ItemDoPedido(produto, quantidade))

    def pagar(self):
        if not self.__status.esta_aberto():
            return False
        if self.__itens.esta_vazia():
            return False
        self.__status = Status("P")
        return True

    def cancelar(self):
        if not self.__status.esta_aberto():
            return False
        self.__status = Status("C")
        return True

    def esta_aberto(self):
        return self.__status.esta_aberto()

    def calcular_desconto(self):
        total = self.__itens.calcular_total()
        return self.__cliente.calcular_desconto(total)

    def calcular_valor_a_pagar(self):
        total = self.__itens.calcular_total()
        return total.subtrair(self.calcular_desconto())

    def calcular_valor_arrecadado(self):
        valor = Dinheiro(0)
        if self.__status.esta_pago():
            valor = self.calcular_valor_a_pagar()
        return valor

    def imprimir(self, numero):
        print("Pedido", numero, "-", self.__cliente.descrever())
        print("  status:", self.__status.descrever())
        self.__itens.imprimir()
        if self.__itens.esta_vazia():
            return
        self.__imprimir_valores()

    def __imprimir_valores(self):
        print("  total:", self.__itens.calcular_total(), "| desconto:", self.calcular_desconto(), "| a pagar:", self.calcular_valor_a_pagar())


# Pedidos: todos os pedidos da loja, guardados pelo numero.
class Pedidos:
    def __init__(self):
        self.__pedidos = {}

    def criar(self, numero, cliente):
        pedido = Pedido(cliente)
        self.__pedidos[numero] = pedido
        return pedido

    def imprimir_relatorio(self):
        for numero, pedido in self.__pedidos.items():
            pedido.imprimir(numero)

    def calcular_arrecadado(self):
        total = Dinheiro(0)
        for pedido in self.__pedidos.values():
            valor = pedido.calcular_valor_arrecadado()
            total = total.somar(valor)
        return total

    def contar_abertos(self):
        todos = self.__pedidos.values()
        abertos = [pedido for pedido in todos if pedido.esta_aberto()]
        return len(abertos)


# --- roteiro da loja -----------------------------------------------------------
pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

ana = Cliente(Pessoa("Ana Souza", Cpf("12345678901"), Email("ana@mail.com")), Endereco("Rua das Flores, 10", "Sorocaba", Cep("18010000")), TipoVip())
pedido_da_ana = pedidos.criar(1, ana)
pedido_da_ana.adicionar_item(caderno, 2)
pedido_da_ana.adicionar_item(caneta, 5)

try:
    bruno = Cliente(Pessoa("Bruno Lima", Cpf("123"), Email("bruno@mail.com")), Endereco("Av. Central, 200", "Votorantim", Cep("18110000")), TipoNormal())
    pedidos.criar(2, bruno)
except ValueError as erro:
    print("pedido 2 recusado:", erro)

segundo_pedido_da_ana = pedidos.criar(3, ana)
segundo_pedido_da_ana.adicionar_item(livro, 1)

try:
    carla = Cliente(Pessoa("Carla Dias", Cpf("98765432100"), Email("carla.mail.com")), Endereco("Rua do Sol, 55", "Sorocaba", Cep("18020000")), TipoFuncionario())
    pedidos.criar(4, carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

diego = Cliente(Pessoa("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com")), Endereco("Rua Nova, 7", "Itu", Cep("13300000")), TipoNormal())
pedido_do_diego = pedidos.criar(5, diego)

eva = Cliente(Pessoa("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com")), Endereco("Alameda Azul, 1", "Itu", Cep("13300001")), TipoFuncionario())
pedido_da_eva = pedidos.criar(6, eva)
pedido_da_eva.adicionar_item(fone, 1)

try:
    fabio = Cliente(Pessoa("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com")), Endereco("Rua Velha, 3", "Itu", Cep("123")), TipoNormal())
    pedidos.criar(7, fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

gil = Cliente(Pessoa("Gil Alves", Cpf("44455566677"), Email("gil@mail.com")), Endereco("Rua do Meio, 9", "Sorocaba", Cep("18030000")), TipoNormal())
pedido_do_gil = pedidos.criar(8, gil)
pedido_do_gil.adicionar_item(fone, 2)

print("pagar 1:", pedido_da_ana.pagar())
print("pagar 3:", segundo_pedido_da_ana.pagar())
print("pagar 5:", pedido_do_diego.pagar())
print("pagar 6:", pedido_da_eva.pagar())
print("cancelar 5:", pedido_do_diego.cancelar())
print("cancelar 1:", pedido_da_ana.cancelar())

pedidos.imprimir_relatorio()
print("arrecadado:", pedidos.calcular_arrecadado())
print("abertos:", pedidos.contar_abertos())
