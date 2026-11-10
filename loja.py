# Loja do TF 11 - passo 5: colecoes de primeira classe (ItensDoPedido e Pedidos).
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


# Cliente: guarda os dados de uma pessoa que compra na loja, em um lugar so.
class Cliente:
    def __init__(self, nome, cpf, email, rua, cidade, cep, tipo):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.rua = rua
        self.cidade = cidade
        self.cep = cep
        self.tipo = tipo      # "N" normal, "V" vip, "F" funcionario


# Produto: o que a loja vende, com nome e preco.
class Produto:
    def __init__(self, nome, preco):
        self.nome = nome
        self.preco = preco


# ItemDoPedido: um produto dentro do pedido e a quantidade comprada dele.
class ItemDoPedido:
    def __init__(self, produto, quantidade):
        self.produto = produto
        self.quantidade = quantidade

    def calcular_subtotal(self):
        return self.produto.preco.multiplicar(self.quantidade)


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
            total = total.somar(item.calcular_subtotal())
        return total

    def imprimir(self):
        for item in self.__itens:
            print("  ", item.quantidade, "x", item.produto.nome, "=", item.calcular_subtotal())


# Pedido: a compra de um cliente, com os itens e o status.
class Pedido:
    def __init__(self, cliente):
        self.cliente = cliente
        self.itens = ItensDoPedido()
        self.status = Status("A")

    def get_status(self):
        return self.status

    def set_status(self, novo_status):
        self.status = novo_status


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
            print("Pedido", numero, "-", pedido.cliente.nome, "-", pedido.cliente.cidade)
            print("  status:", pedido.get_status().descrever())
            pedido.itens.imprimir()
            if not pedido.itens.esta_vazia():
                print("  total:", pedido.itens.calcular_total(), "| desconto:", calcular_desconto(pedido.cliente.tipo, pedido.itens.calcular_total()), "| a pagar:", calcular_valor_a_pagar(pedido))

    def calcular_arrecadado(self):
        total = Dinheiro(0)
        for pedido in self.__pedidos.values():
            if pedido.get_status().esta_pago():
                total = total.somar(calcular_valor_a_pagar(pedido))
        return total

    def contar_abertos(self):
        quantidade = 0
        for pedido in self.__pedidos.values():
            if pedido.get_status().esta_aberto():
                quantidade = quantidade + 1
        return quantidade


def adicionar_item(pedido, produto, quantidade):
    pedido.itens.adicionar(ItemDoPedido(produto, quantidade))


def calcular_desconto(tipo, total):
    if tipo == "V":
        desconto = total.percentual(10)
    elif tipo == "F":
        desconto = total.percentual(20)
    else:
        desconto = Dinheiro(0)
    return desconto


def calcular_valor_a_pagar(pedido):
    return pedido.itens.calcular_total().subtrair(calcular_desconto(pedido.cliente.tipo, pedido.itens.calcular_total()))


def pagar(pedido):
    if pedido.get_status().esta_aberto():
        if not pedido.itens.esta_vazia():
            pedido.set_status(Status("P"))
            return True
        else:
            return False
    else:
        return False


def cancelar(pedido):
    if pedido.get_status().esta_aberto():
        pedido.set_status(Status("C"))
        return True
    else:
        return False


# --- roteiro da loja -----------------------------------------------------------
pedidos = Pedidos()

caderno = Produto("Caderno", Dinheiro(1550))
caneta = Produto("Caneta", Dinheiro(250))
livro = Produto("Livro", Dinheiro(8950))
fone = Produto("Fone", Dinheiro(6000))

ana = Cliente("Ana Souza", Cpf("12345678901"), Email("ana@mail.com"), "Rua das Flores, 10", "Sorocaba", Cep("18010000"), "V")
pedido_da_ana = pedidos.criar(1, ana)
adicionar_item(pedido_da_ana, caderno, 2)
adicionar_item(pedido_da_ana, caneta, 5)

try:
    bruno = Cliente("Bruno Lima", Cpf("123"), Email("bruno@mail.com"), "Av. Central, 200", "Votorantim", Cep("18110000"), "N")
    pedidos.criar(2, bruno)
except ValueError as erro:
    print("pedido 2 recusado:", erro)

segundo_pedido_da_ana = pedidos.criar(3, ana)
adicionar_item(segundo_pedido_da_ana, livro, 1)

try:
    carla = Cliente("Carla Dias", Cpf("98765432100"), Email("carla.mail.com"), "Rua do Sol, 55", "Sorocaba", Cep("18020000"), "F")
    pedidos.criar(4, carla)
except ValueError as erro:
    print("pedido 4 recusado:", erro)

diego = Cliente("Diego Rocha", Cpf("11122233344"), Email("diego@mail.com"), "Rua Nova, 7", "Itu", Cep("13300000"), "N")
pedido_do_diego = pedidos.criar(5, diego)

eva = Cliente("Eva Nunes", Cpf("55566677788"), Email("eva@mail.com"), "Alameda Azul, 1", "Itu", Cep("13300001"), "F")
pedido_da_eva = pedidos.criar(6, eva)
adicionar_item(pedido_da_eva, fone, 1)

try:
    fabio = Cliente("Fabio Costa", Cpf("99988877766"), Email("fabio@mail.com"), "Rua Velha, 3", "Itu", Cep("123"), "N")
    pedidos.criar(7, fabio)
except ValueError as erro:
    print("pedido 7 recusado:", erro)

gil = Cliente("Gil Alves", Cpf("44455566677"), Email("gil@mail.com"), "Rua do Meio, 9", "Sorocaba", Cep("18030000"), "N")
pedido_do_gil = pedidos.criar(8, gil)
adicionar_item(pedido_do_gil, fone, 2)

print("pagar 1:", pagar(pedido_da_ana))
print("pagar 3:", pagar(segundo_pedido_da_ana))
print("pagar 5:", pagar(pedido_do_diego))
print("pagar 6:", pagar(pedido_da_eva))
print("cancelar 5:", cancelar(pedido_do_diego))
print("cancelar 1:", cancelar(pedido_da_ana))

pedidos.imprimir_relatorio()
print("arrecadado:", pedidos.calcular_arrecadado())
print("abertos:", pedidos.contar_abertos())
