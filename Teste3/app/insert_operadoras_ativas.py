import sys
from pathlib import Path
# Adiciona o diretório raiz ao sys.path !!!!!!!!!!!!!!!!!!!
sys.path.append(str(Path(__file__).resolve().parent.parent))

import pandas as pd
from pathlib import Path
from sqlalchemy.orm import Session
from app.config import SessionLocal
from app.models import OperadorasAtivas

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
CSV_PATH_OPERADORAS = RESOURCES_DIR / 'relatorio_cadop.csv'

def insert_operadoras_ativas():
    print("Iniciando inserção de OperadorasAtivas...")

    #Insere os dados do relatorio_cadop na tabela OperadorasAtivas
    if not CSV_PATH_OPERADORAS.exists():
        print("Arquivo relatorio_cadop.csv não encontrado.")
        return

    session = SessionLocal()


    try:
        df = pd.read_csv(CSV_PATH_OPERADORAS, sep=';', encoding='utf-8', dtype=str)

        if df.empty:
            print("O CSV de OperadorasAtivas está vazio.")
            return

        df.columns = df.columns.str.lower()

        print(f"Total de linhas carregadas: {len(df)}")
        print(df.head())  # Exibir primeiras linhas para debug

        dados = df.to_dict(orient='records') #converte em dicionario


        print("Dados a serem inseridos:")
        for d in dados[:5]:
            print(d)

        for dado in dados:
            try:
                registro = OperadorasAtivas(**dado)    
                session.add(registro)
                print(f"Inserido, nome fantasia: {registro.nome_fantasia}" )   
                session.commit()

            except Exception as e:
                print(f"Erro ao inserir registro: {e}")
            
        print(f"Todos os dados inseridos com sucesso!")

    except Exception as e:
        session.rollback()
        print(f"Erro ao processar o arquivo CSV: {e}")

    finally:
        session.close()
        


    #     df['data_registro_ans'] = pd.to_datetime(df['data_registro_ans'], errors='coerce')

    #     for _, row in df.iterrows():
    #         record = OperadorasAtivas(
    #             registro_ans=row['registro_ans'],
    #             cnpj=row['cnpj'],
    #             razao_social=row['razao_social'],
    #             nome_fantasia=row['nome_fantasia'],
    #             modalidade=row['modalidade'],
    #             logradouro=row['logradouro'],
    #             numero=row['numero'],
    #             complemento=row['complemento'],
    #             bairro=row['bairro'],
    #             cidade=row['cidade'],
    #             uf=row['uf'],
    #             cep=row['cep'],
    #             ddd=row['ddd'],
    #             telefone=row['telefone'],
    #             fax=row['fax'],
    #             endereco_eletronico=row['endereco_eletronico'],
    #             representante=row['representante'],
    #             cargo_representante=row['cargo_representante'],
    #             regiao_de_comercializacao=row['regiao_de_comercializacao'],
    #             data_registro_ans=row['data_registro_ans']
    #         )
    #         session.add(record)

    #     session.commit()
    #     print("Dados de OperadorasAtivas inseridos com sucesso!")
    # except Exception as e:
    #     session.rollback()
    #     print(f"Erro ao inserir dados em OperadorasAtivas: {e}")
    # finally:
    #     session.close()


insert_operadoras_ativas()
