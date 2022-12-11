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
                }
            )
        mensagem=msg.produto_lista
        sucesso=True
    except Exception:
        mensagem = f"{msg.erro}: {Exception}"
        sucesso = False
    except:
        mensagem=msg.erro
        sucesso=False
    return RetornoAPI(mensagem,sucesso,produtos)

@app.route('/Produto', methods=['GET'])
def get_produto():
    Id = request.args.get("Id", default=None, type=int)
    produto = list()
    if Id != None:
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
                })
            mensagem=msg.sucesso
            sucesso=True
        except Exception:
            mensagem=f"{msg.erro}: {Exception}"
            sucesso=False
        except:
            mensagem=msg.id_inexistente
            sucesso=False
    else:
        mensagem=msg.id_erro
        sucesso=False
    return RetornoAPI(mensagem,sucesso,produto)

@app.route('/Produto', methods=['POST'])
def new_produtos():
    produto=list()
    try:
        produto = request.json
        my_cursor = mydb.cursor()
        #sql = f"INSERT INTO Produtos (produto, custo, venda, data_cadastro) VALUES ('{produto['produto']}','{produto['custo']}','{produto['venda']}','{datetime.datetime.now()}')"
        sql = f"INSERT INTO Produtos (produto, custo, venda) VALUES ('{produto['produto']}','{produto['custo']}','{produto['venda']}')"
        my_cursor.execute(sql)
        mydb.commit()
        mensagem=msg.produto_cadastro_sucesso
        sucesso=True
    except Exception:
        mensagem = f"{msg.erro}: {Exception}"
        sucesso = False
    except:
        mensagem=msg.erro
        sucesso=False
    return RetornoAPI(mensagem,sucesso,produto)

app.run(host='0.0.0.0')