from sqlalchemy import Column, Integer, String, Date, Float
from datetime import date
from typing import Union
from model import Base


class Pagamento(Base):
    __tablename__ = 'pagamento'

    id = Column("pk_pagamento", Integer, primary_key=True)
    nome = Column (String(4000))
    descricao = Column(String(4000))
    data_vencimento = Column(Date)
    data_pagamento = Column(Date)
    valor = Column(Float)
    valor_multa = Column(Float)
    status = Column(String(4000))
    

    def __init__(self, nome:str, descricao:str, data_vencimento:date,
                 data_pagamento:date, valor:float, valor_multa:float, status:str):
        self.nome = nome
        self.descricao = descricao
        self.data_vencimento = data_vencimento
        self.data_pagamento = data_pagamento
        self.valor = valor
        self.valor_multa = valor_multa
        self.status = status