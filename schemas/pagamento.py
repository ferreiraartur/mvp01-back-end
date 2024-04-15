from unicodedata import category
from pydantic import BaseModel
from typing import Optional, List
from datetime import date
from model.pagamento import Pagamento


class PagamentoSchema(BaseModel):
    """ Define como um novo pagamento a ser inserido deve ser representado
    """
    id: int = "1"
    nome: str = "Conta de Luz"
    descricao: Optional[str] = " casa"
    data_vencimento: date = (2024-4-5)
    data_pagamento: date = (2024-4-5)
    status: str = "Aberto"
    valor: float = 1
    valor_multa: float = 0

class PagamentoBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do pagamento.
    """
    nome: str = "Conta de Luz"

class PagamentoBuscaPorIdSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do pagamento.
    """
    id: int = "1"

class ListagemPagamentosSchema(BaseModel):
    """ Define como uma listagem de pagamentos será retornada.
    """
    pagamentos:List[PagamentoSchema]


def apresenta_pagamentos(pagamentos: List[Pagamento]):
    """ Retorna uma representação dos pagamentos seguindo o schema definido em
        ProdutoViewSchema.
    """
    result = []
    for pagamento in pagamentos:
        result.append({
            "id": pagamento.id,
            "nome": pagamento.nome,
            "descricao": pagamento.descricao,
            "data_vencimento": pagamento.data_vencimento,
            "data_pagamento": pagamento.data_pagamento,
            "status": pagamento.status,
            "valor": pagamento.valor,
            "valor_multa": pagamento.valor_multa,
        })
    return {"pagamentos": result}


class PagamentoViewSchema(BaseModel):
    id: int = 1
    nome: str = "Conta de Luz"
    descricao: Optional[str] = "Conta de Luz "
    data_vencimento: date = (2024, 4, 5)
    data_pagamento: date = (2024, 4, 5)
    status: str = "Aberto"
    valor: float = 1
    valor_multa: float = 0


class PagamentoDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    mesage: str
    #nome: str
    id: int


def apresenta_pagamento(pagamento: Pagamento):
    """ Retorna uma representação do pagamento seguindo o schema definido em
        PagamentoViewSchema.
    """
    return {
        "nome": pagamento.nome,
        "descricao": pagamento.descricao,
        "data_vencimento": pagamento.data_vencimento,
        "data_pagamento": pagamento.data_pagamento,
        "status": pagamento.status,
        "valor": pagamento.valor,
        "valor_multa": pagamento.valor_multa,
    }



