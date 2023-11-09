# Projeto da AV3 da cadeira de prog. Funcional.
---

## Situando
---
Nossa API de saldos atua como backend para um sistema de gerenciamento financeiro para um cliente. Nela, o usuário terá as seguintes possibilidades;

#### Contas a pagar / receber
---
É um conceito muito utilizado no financeiro. A pagar seriam todas as contas que estão por vir e que serão pagas pelo usuário, como contas de luz, faturas e afins. E as contas a receber são aquelas que vem como um pagamento para o usuário, como um pix que ele vai receber de alguém, ou o recebimento de mais uma parcela de uma venda que ele fez. 

1. Cadastrar suas contas(pagar/receber).
3. Editar ou remover suas contas.
2. Listar todas as suas contas.
3. Consultar seu saldo(do dia, ou com previsão).

# Para rodar o projeto:

1. pip install nas dependencias
    (irei listá-las para melhorar aqui)

```uvicorn main:app --reload```


''''

    API DE SALDOS

    autenticar -> (post) => 
        { 
            login: numero - "cpf",
            senha: string - "hash" 
        } 
        retorna JWT (id do cliente, expiracao)
    
    consultarSaldo -> (post) => 
        {
            token : string "jwt",
            dia: date 
        }
        retorna saldo atual da conta caso não tenha data, caso tenha, faz uma varredura das contas a pagar e a receber para dizer o saldo 
        da conta no dia selecionado.

    cadastrarConta -> (post) =>
        {
            token : string "jwt",   
            conta:  {
                tipo: string "p" para pagar | "r" para receber,
                descricao: "string",
                valor: number,
            }
        } 
        retorna o objeto criado no banco de dados seguindo as especificações do corpo da requisição

    cadastrarConta -> (post) =>
        {
            token : string "jwt",   
            conta:  {
                tipo: string "p" para pagar | "r" para receber,
                descricao: "string",
                valor: number,
            }
        } 
        retorna o objeto criado no banco de dados seguindo as especificações do corpo da requisição

    deletarConta -> (post) => 
        {
            token : string "jwt",   
            idConta: number,
        }
        retorna status para caso tenha deletado

'''
