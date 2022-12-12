from flask import Flask, make_response, request, jsonify
from bd import mydb
import mensagem as msg
import datetime
print(datetime.datetime.now())
app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

def RetornoAPI(mensagem,sucesso,dados):
    return make_response(jsonify(
        mensagem=mensagem,
        sucesso=sucesso,
        dados=dados
    ))

def verifica_id(Id):
    my_cursor = mydb.cursor()
    sql = f"SELECT IF(EXISTS(SELECT * FROM Produtos WHERE id = {Id}), {Id}, FALSE)"
    my_cursor.execute(sql)
    return my_cursor.fetchall()[0][0]

@app.route('/')
def connection():
    return 'Conectado'

@app.route('/Produtos', methods=['GET'])
def get_produtos():
    produtos = list()
    try:
        my_cursor = mydb.cursor()
        sql = "SELECT * FROM Produtos"
        my_cursor.execute(sql)
        dados = my_cursor.fetchall()
        for produto in dados:
            produtos.append(
                {
                    'id': produto[0],
                    'produto': produto[1],
                    'custo': produto[2],
                    'venda': produto[3],
                    'data_cadastro': produto[4],
                    'data_alteracao': produto[5],
                    'quantidade': produto[6]
                }
            )
        mensagem=msg.produto_lista
        sucesso=True
    except Exception:
        mensagem = f"{msg.erro}: {Exception}"
        sucesso = False
        produtos=""
    except:
        mensagem=msg.erro
        sucesso=False
        produtos=""
    return RetornoAPI(mensagem,sucesso,produtos)

@app.route('/Produto', methods=['GET'])
def get_produto():
    Id = request.args.get("Id", default=None, type=int)
    produto = list()
    Id = verifica_id(Id)
    if Id != None and Id > 0:
        try:
            my_cursor = mydb.cursor()
            sql = f"SELECT * FROM Produtos WHERE id={Id}"
            my_cursor.execute(sql)
            dados = my_cursor.fetchall()[0]
            produto.append(
                {
                    'id': dados[0],
                    'produto': dados[1],
                    'custo': dados[2],
                    'venda': dados[3],
                    'data_cadastro': dados[4],
                    'data_alteracao': dados[5],
                    'quantidade': dados[6]
                })
            mensagem=msg.sucesso
            sucesso=True
        except Exception:
            mensagem=f"{msg.erro}: {Exception}"
            sucesso=False
            produto = ""
    else:
        mensagem=msg.id_inexistente
        sucesso=False
        produto=""
    return RetornoAPI(mensagem,sucesso,produto)

@app.route('/ProdutoUpdate', methods=['POST'])
def update_produto():
    produto = request.json
    Id = verifica_id(produto['id'])
    if Id != None and Id > 0:
        try:
            my_cursor = mydb.cursor()
            sql = f"UPDATE Produtos SET " \
                  f'produto = "{produto["produto"]}", ' \
                  f"custo = {produto['custo']}, " \
                  f"venda = {produto['venda']}, " \
                  f'data_alteracao = "{datetime.datetime.now()}", ' \
                  f"quantidade = {produto['quantidade']} " \
                  f"WHERE id={produto['id']}"
            my_cursor.execute(sql)
            mydb.commit()
            mensagem=msg.sucesso
            sucesso=True
        except Exception:
            mensagem=f"{msg.erro}: {Exception}"
            sucesso=False
            produto = ""
        except:
            mensagem=msg.id_inexistente
            sucesso=False
            produto = ""
    else:
        mensagem=msg.id_inexistente
        sucesso=False
        produto=""
    return RetornoAPI(mensagem,sucesso,produto)

@app.route('/Produto', methods=['POST'])
def new_produtos():
    try:
        produto = request.json
        my_cursor = mydb.cursor()
        sql = f"INSERT INTO Produtos (produto, custo, venda, quantidade, data_cadastro, data_alteracao) " \
              f"VALUES ('{produto['produto']}'," \
              f"'{produto['custo']}'," \
              f"'{produto['venda']}'," \
              f"'{produto['quantidade']}'," \
              f"'{datetime.datetime.now()}'," \
              f"'{datetime.datetime.now()}')"
        my_cursor.execute(sql)
        mydb.commit()
        mensagem=msg.produto_cadastro_sucesso
        sucesso=True
    except Exception:
        mensagem = f"{msg.erro}: {Exception}"
        sucesso = False
        produto=""
    except:
        mensagem=msg.erro
        sucesso=False
        produto=""
    return RetornoAPI(mensagem,sucesso,produto)

app.run(host='0.0.0.0')