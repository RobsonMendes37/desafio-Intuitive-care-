from fastapi import APIRouter, HTTPException, Query, status
from typing import List
from app.models.Operadoras_Ativas import OperadorasAtivasBase
import logging
import pandas as pd
from pathlib import Path

ERROR_DETAIL = "Some error occurred: {e}"
NOT_FOUND = "Not found"

logger = logging.getLogger("app_logger")

router = APIRouter()

# Caminho do arquivo CSV
CSV_FILE_PATH = Path("C:/Users/robso/Documents/desafio-intuitive-care/Teste4/resources/Relatorio_cadop.csv")

# Carregar os dados do CSV na inicialização
try:
    if CSV_FILE_PATH.exists():
        operadoras_df = pd.read_csv(CSV_FILE_PATH, sep=";", encoding="utf-8", dtype=str)  # Força tudo como string
        operadoras_df = operadoras_df.where(pd.notna(operadoras_df), None)  # Substitui NaN por None
        logger.info(f"Arquivo {CSV_FILE_PATH.name} carregado com {len(operadoras_df)} registros.")
    else:
        operadoras_df = None
        logger.warning(f"Arquivo {CSV_FILE_PATH} não encontrado.")
except Exception as e:
    logger.error(f"Erro ao carregar o CSV: {e}")
    operadoras_df = None




@router.get("/", response_description="Recupera Operadoras Ativas", response_model=List[OperadorasAtivasBase])
async def read_operadoras(
    page: int = Query(1, ge=1, description="Página da paginação, começando em 1"),
    limit: int = Query(100, le=100, ge=1, description="Itens por página (1-100)")
):
    """Retorna as operadoras ativas  paginadas."""
    if operadoras_df is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao carregar o CSV. Verifique se o arquivo existe e está no formato correto."
        )

    try:
        total_registros = len(operadoras_df)
        total_paginas = (total_registros // limit) + (1 if total_registros % limit > 0 else 0)

        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        if start_idx >= total_registros:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Página fora do alcance. Total de páginas disponíveis: {total_paginas}"
            )

        operadoras_paginadas = operadoras_df.iloc[start_idx:end_idx].copy()

        # Renomear as colunas para corresponder ao modelo Pydantic
        operadoras_paginadas.rename(columns={
            "Registro_ANS": "registro_ans",
            "CNPJ": "cnpj",
            "Razao_Social": "razao_social",
            "Nome_Fantasia": "nome_fantasia",
            "Modalidade": "modalidade",
            "Logradouro": "logradouro",
            "Numero": "numero",
            "Complemento": "complemento",
            "Bairro": "bairro",
            "Cidade": "cidade",
            "UF": "uf",
            "CEP": "cep",
            "DDD": "ddd",
            "Telefone": "telefone",
            "Fax": "fax",
            "Endereco_eletronico": "endereco_eletronico",
            "Representante": "representante",
            "Cargo_Representante": "cargo_representante",
            "Regiao_de_Comercializacao": "regiao_de_comercializacao",
            "Data_Registro_ANS": "data_registro_ans"
        }, inplace=True)

        # 🔹 Substituir "None" (string) por None (valor real do Python)
        operadoras_paginadas.replace({"None": None, "nan": None}, inplace=True)

        # 🔹 Converter DataFrame para lista de dicionários
        registros = operadoras_paginadas.to_dict(orient="records")

        return registros
    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao recuperar Operadoras: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {e}")
    




@router.get("/buscar", response_description="Busca operadoras por razão social", response_model=List[OperadorasAtivasBase])
async def buscar_operadoras_por_razao_social(
    q: str = Query(..., min_length=3, description="Nome da operadora a ser buscado"),
    page: int = Query(1, ge=1, description="Página da paginação, começando em 1"),
    limit: int = Query(100, le=100, ge=1, description="Itens por página (1-100)")
):
    """Busca operadoras pelo Razão Social."""

    if operadoras_df is None:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro ao carregar o CSV. Verifique se o arquivo existe e está no formato correto."
        )

    try:
        q_lower = q.lower()
        # Filtrar registros onde 'razao_social' contém o termo de busca
        operadoras_df["Razao_Social"] = operadoras_df["Razao_Social"].astype(str).str.lower()
        resultados = operadoras_df[operadoras_df["Razao_Social"].str.contains(q_lower, na=False)]
        total_registros = len(resultados)
        total_paginas = (total_registros // limit) + (1 if total_registros % limit > 0 else 0)

        # Paginação
        start_idx = (page - 1) * limit
        end_idx = start_idx + limit

        if start_idx >= total_registros:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Pesquisa não encontrada. Total de páginas disponíveis: {total_paginas}"
            )

        resultados_paginados = resultados.iloc[start_idx:end_idx].copy()

        # Renomear colunas para corresponder ao modelo Pydantic
        resultados_paginados.rename(columns={
            "Registro_ANS": "registro_ans",
            "CNPJ": "cnpj",
            "Razao_Social": "razao_social",
            "Nome_Fantasia": "nome_fantasia",
            "Modalidade": "modalidade",
            "Logradouro": "logradouro",
            "Numero": "numero",
            "Complemento": "complemento",
            "Bairro": "bairro",
            "Cidade": "cidade",
            "UF": "uf",
            "CEP": "cep",
            "DDD": "ddd",
            "Telefone": "telefone",
            "Fax": "fax",
            "Endereco_eletronico": "endereco_eletronico",
            "Representante": "representante",
            "Cargo_Representante": "cargo_representante",
            "Regiao_de_Comercializacao": "regiao_de_comercializacao",
            "Data_Registro_ANS": "data_registro_ans"
        }, inplace=True)

        #  Substituir "None" (string) por None (valor real do Python)
        resultados_paginados.replace({"None": None, "nan": None}, inplace=True)

        return resultados_paginados.to_dict(orient="records")

    except HTTPException as e:
        raise e
    except Exception as e:
        logger.error(f"Erro ao buscar Operadoras: {e}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro inesperado: {e}")
