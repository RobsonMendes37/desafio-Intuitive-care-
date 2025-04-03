from sqlalchemy import Column, Integer, String, Numeric, Date
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class DemonstracoesContabeis(Base):
    __tablename__ = 'demonstracoes_contabeis'
    id = Column(Integer, primary_key=True, autoincrement=True)
    data = Column(Date, nullable=False)
    reg_ans = Column(String, nullable=False)
    cd_conta_contabil = Column(String, nullable=False)
    descricao = Column(String, nullable=False)
    vl_saldo_inicial = Column(Numeric, nullable=False)
    vl_saldo_final = Column(Numeric, nullable=False)

class OperadorasAtivas(Base):
    __tablename__ = 'operadoras_ativas'
    id = Column(Integer, primary_key=True, autoincrement=True)
    registro_ans = Column(String, nullable=False, unique=True)
    cnpj = Column(String, nullable=False)
    razao_social = Column(String, nullable=False)
    nome_fantasia = Column(String, nullable=True)
    modalidade = Column(String, nullable=True)
    logradouro = Column(String, nullable=True)
    numero = Column(String, nullable=True)
    complemento = Column(String, nullable=True)
    bairro = Column(String, nullable=True)
    cidade = Column(String, nullable=True)
    uf = Column(String, nullable=True)
    cep = Column(String, nullable=True)
    ddd = Column(String, nullable=True)
    telefone = Column(String, nullable=True)
    fax = Column(String, nullable=True)
    endereco_eletronico = Column(String, nullable=True)
    representante = Column(String, nullable=True)
    cargo_representante = Column(String, nullable=True)
    regiao_de_comercializacao = Column(String, nullable=True)
    data_registro_ans = Column(Date, nullable=True)
