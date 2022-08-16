rs
from datetime import date
import matplotlib.pyplot as plt

conexao = pymysql.connect(
    host='localhost',
    user='root',
    password='1234',
    db='projetosozinho',
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


def Menu(lista):
    Cabeçalho('MENU PRINCIPAL')
    c = 1
    for item in lista:
        print(f' {c} - {item}')
        c += 1
    print(Linha())
    opcao = LeiaInt('Digite uma opçao desejada!')
    return opcao


def LeiaInt(mensagem):
    while True:
        try:
            n = int(input(mensagem))
        except (ValueError, TypeError):
            print('Por favor, digite um número válido para continuar!')
        return n


def Linha(tam=42):
    return '-' * tam


def Cabecalho(txt):
    print(Linha())
    print(txt.center(42))
    print(Linha())


def LogarCadastrar(): #esta opção o usuario podera cadastrar, porém terá limite de funções dependendo do nivel do usuario.
    usuarios = 0
    autenticado = False
    usuarioMajoritario = False
    if resposta == 1:
        nome = str(input('Digite o nome do usuário:  '))
        senha = str(input('Digite sua senha: '))
        for linha in banco:
            if nome == linha['nome'] and senha == linha['senha']:
                autenticado = True
                print(f'Bem vindo ao programa {linha["nome"]}!')
                if linha[
                    'nivel'] == 1:  # isso é para proteger o sitema da empresa, para somente quem tiver a senha de gerente podera visualizar dados de vendas e alterar produtos e seus respectivos preços
                    usuarioMajoritario = False
                elif linha['nivel'] == 2:
                    usuarioMajoritario = True
                break

            else:
                autenticado = False
        if not autenticado:
            print('Nome ou senha não conferem! Tente novamente!')
    elif resposta == 2:
        print('Faça seu cadastro: ')
        while True:
            nome = str(input('Digite o nome do usuario: '))
            senha = str(input('Digite sua senha: '))
            senha2 = str(input('Digite a senha novamente: '))
            if senha != senha2:
                print('As senhas não conferem!')
            else:
                break
        for linha in banco:
            if nome == linha['nome'] and senha == linha['senha']:
                usuarioExistente = 1
        if usuarios == 1:
            print('Usuario já foi cadastrado! Tente um novo usuario!')
        elif usuarios == 0:
            try:
                with conexao.cursor() as cursor:
                    cursor.execute('insert into usuarios (nome, senha, nivel) values(%s,%s,%s)',
                                   (nome, senha, 1))  # sempre um novo cadastrado tera acesso restrito
                    conexao.commit()  # fazendo alterações dentro do meu banco de dados sql
                print('Usuario cadastrado com sucesso!')
            except:
                print('Erro ao se conctar com o banco de dados!')
    else:
        print('Digite uma opção valida para ser executada!')
    return autenticado, usuarioMajoritario


def CadastrarClientes():
    nome = str(input('Nome: '))
    idade = int(input('Idade: '))
    sexo = str(input('Sexo [M/F]: ')).strip().upper()[0]
    endereco = str(input('Endereço: '))
    bairro = str(input('Bairro: '))
    celular = int(input('Celular: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute(
                'insert into cadastros_clientes (nome,idade,sexo,endereco,bairro,celular) values(%s,%s,%s,%s,%s,%s)',
                (nome, idade, sexo, endereco, bairro, celular))
            conexao.commit()
        print(f'Cliente {nome} cadastrado com sucesso!')
    except:
        print('Erro ao Cadastrar novo cliente!')


def ListarClientes():
    clientes = []
    clientesPesquisados = []
    pesquisa = str(input('Digite o nome do cliente a ser pesquisado: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from cadastros_clientes')
            clientesCadastrados = cursor.fetchall()
    except:
        print('Não foi possivel encontrar este cliente no banco de dados')
    for i in clientesCadastrados:
        clientes.append(i)
    if len(clientes) != 0:
        qtd = 0
        for i in range(0, len(clientes)):
            if pesquisa in clientes[i]['nome']:
                clientesPesquisados.append(clientes[i])
                qtd += 1
        if qtd > 0:
            for i in clientesPesquisados:
                print(f'o cliente {i["nome"]} {i["celular"]}')
        else:
            print(f'Nao foi encontrado nenhum cliente chamado {pesquisa}')

    else:
        print('nenhum cliente cadastrado')


def Vendas():
    produto_id = 0
    print(Linha())
    while True:
        print('''
        1	Progressiva
        2	Progressiva
        3	Escova
        4	Selagem
        5	Selagem
        6	Hidratação
        7	Hidrataçao
        8	Corte
        9	Mechas
        10	Mechas
        11	Luzes
        12	Luzes
        13	Detox
        14	Reconstrucao''')

        produto_id = int(input('Digite o ID do produto vendido:  '))
        nome_produto = str(input('Digite o nome do produto ou serviço realizado: '))
        nome_cliente = str(input('Digite o nome completo do Cliente: '))
        valor_venda = LeiaInt('Digite o valor da venda: R$ ')
        data = date.today()
        if produto_id < 0 or produto_id > 15:
            print('Por favor, digite um ID de produto valido.')
        else:
            break


    try:
        with conexao.cursor() as cursor:
            cursor.execute(' insert into vendas (id_produto,produto,nome,data_venda,valor_venda) values (%s,%s,%s,%s,%s)', (produto_id,nome_produto,nome_cliente,data,valor_venda))
            conexao.commit()
        print('Venda cadastrada com sucesso!')
    except:
        print('Não foi posssivel se conectar ao banco de dados produtos e servicos')



def GerarEstatistica():
    nome_produtos = []
    nome_produtos.clear()
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from servicos_e_produtos')
            Produtos = cursor.fetchall()
    except:
        print('Erro ao fazer consulta no banco de dados!')
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from vendas')
            vendido = cursor.fetchall()
    except:
        print('Erro ao fazer consulta dentro da tabela vendas!')

    for i in Produtos:
        nome_produtos.append(i['produto'])
    valores = []
    valores.clear()
    for h in range(0,len(nome_produtos)):
        somaValor = -1
        for i in vendido :
            if i['produto'] == nome_produtos[h]:
                somaValor += i['valor_venda']
        if somaValor == -1:
            valores.append(0)
        elif somaValor > 0:
            valores.append(somaValor +1)
    plt.bar(nome_produtos, valores, color = 'red')
    plt.ylabel('Quantidade vendida em reais')
    plt.xlabel('produtos')
    plt.title('Estatistica de vendas do Salão')
    plt.show()





autentico = False
while not autentico:
    Cabecalho('SALÃO DO DOUGLAS')
    Cabecalho('menu principal')
    print('''
    [1] Fazer Login
    [2] Fazer Cadastro de usuário''')
    print(Linha())
    resposta = int(input('Digite uma opçao desejada: '))
    try:
        with conexao.cursor() as cursor:
            cursor.execute('select * from usuarios')
            banco = cursor.fetchall()
    except:
        print('Erro ao conectar com o banco de dados Usuarios!')
    autentico, usuarioSupremo = LogarCadastrar()

if autentico:
    print('Autenticado')
    decisaoUsuario = 1
    while decisaoUsuario != 0:
        print(Linha())
        print('''
        [0] Sair
        [1] Cadastrar novo clinte
        [2] Pesquisar por nome do cliente  
        [3] Efetuar Venda 
        [4] Ver estatistica das vendas ''')

        print(Linha())
        decisaoUsuario = int(input('Digite uma opção valida: '))
        if usuarioSupremo == True:
            if decisaoUsuario == 1:
                CadastrarClientes()
            if decisaoUsuario == 2:
                ListarClientes()
            if decisaoUsuario == 4:
                GerarEstatistica()
        else:
            print('Esta função não esta liberada para este usuario!')
        if decisaoUsuario == 3:
            Vendas()