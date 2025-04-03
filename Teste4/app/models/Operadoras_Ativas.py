from typing import Union, Optional
from pydantic import BaseModel
from datetime import date

class OperadorasAtivasBase(BaseModel):
    registro_ans: Union[str, int]
    cnpj: Union[str, int]
    razao_social: str
    nome_fantasia: Optional[str] = None
    modalidade: Optional[str] = None
    logradouro: Optional[str] = None
    numero: Optional[str] = None
    complemento: Optional[str] = None
    bairro: Optional[str] = None
    cidade: Optional[str] = None
    uf: Optional[str] = None
    cep: Union[str, int, None] = None
    ddd: Union[str, int, None] = None
    telefone: Union[str, int, None] = None
    fax: Optional[Union[str, int]] = None
    endereco_eletronico: Optional[str] = None
    representante: Optional[str] = None
    cargo_representante: Optional[str] = None
    regiao_de_comercializacao: Optional[Union[str, float, int]] = None
    data_registro_ans: Optional[date] = None
