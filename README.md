# TF 11 - Object Calisthenics

Refatoracao da loja feia aplicando as regras do Object Calisthenics, sem mudar o que o programa imprime. Para conferir:

```
py loja.py > saida-nova.txt
diff saida-original.txt saida-nova.txt
```

## 1. Normalizacao

Normalizar e deixar cada informacao guardada em um lugar so e fazer o resto apontar pra ela. Na loja feia os dados da Ana estavam copiados no pedido 1 e no pedido 3, entao se ela mudasse de endereco teria que mudar nos dois. Agora existe um objeto Cliente da Ana e os dois pedidos apontam pra ele (o mesmo vale pro Produto, o Fone tem o preco em um lugar so).

## 2. Obsessao por tipos primitivos

O Cpf virou classe porque como string qualquer coisa passava, ate o "123". Com a classe a regra dos 11 caracteres fica no construtor e nao da pra existir um Cpf invalido no programa, o erro aparece na hora que cria. O Dinheiro guarda centavos em int porque float erra conta (0.1 + 0.2 nao da 0.3) e com centavos inteiros a conta sempre fecha.

## 3. Diga, nao pergunte

Antes o codigo perguntava o status com get_st e trocava com set_st de fora do pedido. Agora eu so chamo pedido.pagar() ou pedido.cancelar() e o proprio Pedido ve se pode (se esta aberto e se tem itens) e devolve True ou False. Fica melhor porque a regra fica num lugar so e ninguem de fora consegue deixar o pedido num status errado.

## 4. Fail first

O hadouken era a funcao valida, com um if dentro do outro pra email, cpf e cep, e tambem o pagar. A validacao foi pros construtores de Email, Cpf e Cep, e o pagar() agora testa os casos de erro primeiro e sai com return False. O else foi trocado por retorno antecipado porque fica tudo num nivel so e mais facil de ler, e o if/elif do desconto virou polimorfismo (TipoNormal, TipoVip e TipoFuncionario), entao pra criar um tipo novo e so criar outra classe sem mexer nas outras.

## 5. Modularizacao

- Cpf: valida e guarda o cpf.
- Email: valida e guarda o email.
- Cep: valida e guarda o cep.
- Dinheiro: guarda o valor em centavos e faz as contas e a impressao em R$.
- Status: guarda o status do pedido e sabe a descricao dele.
- Pessoa: nome, cpf e email de alguem.
- Endereco: rua, cidade e cep.
- TipoNormal: cliente sem desconto.
- TipoVip: cliente com 10% de desconto.
- TipoFuncionario: funcionario com 20% de desconto.
- Cliente: junta pessoa, endereco e tipo e calcula o desconto.
- Produto: nome e preco do que a loja vende.
- ItemDoPedido: um produto com a quantidade e o subtotal.
- ItensDoPedido: a lista de itens de um pedido e o total dela.
- Pedido: a compra de um cliente, sabe pagar, cancelar e se imprimir.
- Pedidos: todos os pedidos pelo numero, faz o relatorio, o arrecadado e conta os abertos.

## 6. Divida tecnica

Ficou uma divida: no roteiro so os pedidos 2, 4 e 7 estao dentro de try/except, porque eu ja sei que eles sao os recusados. Se um cliente "bom" tivesse dado erro o programa ia parar. O certo seria uma forma de criar cliente e pedido que sempre trata o erro, custa pouco (uma funcao a mais no roteiro) e eu pagaria se a loja passasse a receber dados de fora. A regra mais dificil foi a de um ponto por linha, porque varias vezes tive que criar metodos so pra um objeto perguntar pro outro.
