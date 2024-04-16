from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote
from sqlalchemy.exc import IntegrityError
from model import Session, Pagamento
from logger import logger
from schemas import *
from flask_cors import CORS


info = Info(title="API Back-End", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# definindo tags
pagamento_tag = Tag(name="Pagamento", description="Adição, visualização e remoção de pagamentos à base")


@app.get('/')
def home():
    return redirect('/openapi')


@app.post('/pagamento', tags=[pagamento_tag],
          responses={"200": PagamentoViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_pagamento(form: PagamentoSchema):
    """Adiciona um novo Pagamento à base de dados

    Retorna uma representação dos pagamentos associados.
    """
    pagamento = Pagamento(
        nome=form.nome,
        descricao=form.descricao,
        data_vencimento=form.data_vencimento,
        data_pagamento=form.data_pagamento,
        status=form.status,
        valor=form.valor,
        valor_multa=form.valor_multa)
    logger.debug(f"Adicionando pagamento de nome: '{pagamento.nome}'")
    try:
        # criando conexão com a base
        session = Session()
        # adicionando pagamento
        session.add(pagamento)
        # efetivando o camando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionado pagamento de nome: '{pagamento.nome}'")
        return apresenta_pagamento(pagamento), 200

    except IntegrityError as e:
        # como a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Pagamento de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar pagamento '{pagamento.nome}', {error_msg}")
        return {"mesage": error_msg}, 409

    except Exception as e:
        # caso um erro fora do previsto
        error_msg = "Não foi possível salvar novo item :/"
        logger.warning(f"Erro ao adicionar pagamento '{pagamento.nome}', {error_msg}")
        return {"mesage": error_msg}, 400


@app.get('/pagamentos', tags=[pagamento_tag],
         responses={"200": ListagemPagamentosSchema, "404": ErrorSchema})
def get_pagamentos():
    """Faz a busca por todos os pagamentos cadastrados

    Retorna uma representação da listagem de pagamentos.
    """
    logger.debug(f"Coletando pagamentos ")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pagamentos = session.query(Pagamento).all()

    if not pagamentos:
        # se não há pagamentos cadastrados
        return {"pagamentos": []}, 200
    else:
        logger.debug(f"%d pagamentos econtrados" % len(pagamentos))
        # retorna a representação de pagamento
        print(pagamentos)
        return apresenta_pagamentos(pagamentos), 200


@app.get('/pagamento', tags=[pagamento_tag],
         responses={"200": PagamentoViewSchema, "404": ErrorSchema})
def get_pagamento(query: PagamentoBuscaSchema):
    """Faz a busca por um Pagamento a partir do nome do pagamento

    Retorna uma representação dos pagamentos e aaa associados.
    """
    pagamento_nome = unquote(unquote(query.nome))
    print(pagamento_nome)
    logger.debug(f"Coletando dados sobre pagamento #{pagamento_nome}")
    # criando conexão com a base
    session = Session()
    # fazendo a busca
    pagamento = session.query(Pagamento).filter(Pagamento.nome == pagamento_nome).first()

    if not pagamento:
        # se o pagamento não foi encontrado
        error_msg = "Pagamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar pagamento '{pagamento_nome}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pagamento econtrado: '{pagamento.nome}'")
        # retorna a representação de pagamento
        return apresenta_pagamento(pagamento), 200


@app.post('/atualizar_status_pagamento', tags=[pagamento_tag],
            responses={"200": PagamentoViewSchema, "404": ErrorSchema})
def update_status_pagamento(query: PagamentoBuscaPorIdSchema):
    """Atualiza o status de um Pagamento a partir do id informado

    Retorna uma mensagem de confirmação da atualização.
    """
    pagamento_id = query.id
    logger.debug(f"Coletando dados sobre pagamento#{pagamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a atualização
    pagamento = session.query(Pagamento).filter(Pagamento.id == pagamento_id).first()
    logger.debug(f"exibir pagamento#{pagamento}")
    pagamento.status = "Quitado"
    session.commit()

    if not pagamento:
        # se o pagamento não foi encontrado
        error_msg = "Pagamento não encontrado na base :/"
        logger.warning(f"Erro ao buscar pagamento '{pagamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404
    else:
        logger.debug(f"Pagamento econtrado: '{pagamento.nome}'")
        # retorna a representação de pagamento
        return apresenta_pagamento(pagamento), 200
    

@app.delete ('/pagamento', tags=[pagamento_tag],
        responses={"200": PagamentoViewSchema, "404": ErrorSchema})
def del_pagamento(query: PagamentoBuscaPorIdSchema):
    """Deleta um Pagamento a partir do id do pagamento informado
    Retorna uma mensagem de confirmação da remoção.
    """
    pagamento_id = query.id
    logger.debug(f"Coletando dados sobre produto #{pagamento_id}")
    # criando conexão com a base
    session = Session()
    # fazendo a remoção
    count = session.query(Pagamento).filter(Pagamento.id == pagamento_id).delete()
    session.commit()

    if count:
        # retorna a representação da mensagem de confirmação
        logger.debug(f"Deletado produto #{pagamento_id}")
        return {"mesage": "Produto removido", "id": pagamento_id}
    else:
        # se o produto não foi encontrado
        error_msg = "Produto não encontrado na base :/"
        logger.warning(f"Erro ao deletar produto #'{pagamento_id}', {error_msg}")
        return {"mesage": error_msg}, 404
