import sys
from pathlib import Path
# Adiciona o diretório raiz ao sys.path !!!!!!!!!!!!!!!!!!!
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models import DemonstracoesContabeis, OperadorasAtivas

BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
CSV_PATH_UNIFICADO = RESOURCES_DIR / 'demonstracoes_contabeis_unificado.csv'

def insert_demonstracoes_contabeis():
    print("Iniciando inserção de DemonstracoesContabeis...")

    if not CSV_PATH_UNIFICADO.exists():
        print("Arquivo CSV unificado não encontrado. Execute extract_and_merge() primeiro.")
        return

    print(f"Verificando arquivo CSV em: {CSV_PATH_UNIFICADO}")

    session = SessionLocal()

    try:
        df = pd.read_csv(CSV_PATH_UNIFICADO, sep=';', encoding='utf-8')
        print(f"Total de linhas carregadas: {len(df)}")
        print(df.head())  # Exibir primeiras linhas para debug

        if df.empty:
            print("O CSV unificado está vazio. Verifique a extração dos dados.")
            return

        df['data'] = pd.to_datetime(df['data'], errors='coerce')
        df['vl_saldo_inicial'] = df['vl_saldo_inicial'].str.replace(',', '.', regex=True).astype(float)
        df['vl_saldo_final'] = df['vl_saldo_final'].str.replace(',', '.', regex=True).astype(float)

        dados = df.to_dict(orient="records")  # Converte o DataFrame para lista de dicionários

        # Logando os primeiros registros para depuração
        print(" Dados a serem inseridos (exemplo):")
        for d in dados[:5]:  # Exibe os 5 primeiros registros
            print(d)

        contador = 0
        batch_size = 1000  # buffer

        for dado in dados:
            try:
                registro = DemonstracoesContabeis(**dado)  
                session.add(registro)
                print(f"Inserindo id,data,reg_ans: {registro.id,registro.data,registro.reg_ans}")  # Log  
                contador += 1

                # Faz commit a cada 1000 inserções para melhorar a performance
                if contador % batch_size == 0:
                    session.commit()
                    print(f"Commit realizado após {contador} registros.")

            except Exception as e:
                print(f"Erro ao inserir {dado}: {e}")

        # Faz commit final para inserir registros restantes
        session.commit()
        print(f"Commit final realizado! Total de registros inseridos: {contador}")

    except Exception as e:
        session.rollback()
        print(f"Erro ao inserir dados: {e}")
    finally:
        session.close()


#Descomente para testar
insert_demonstracoes_contabeis()