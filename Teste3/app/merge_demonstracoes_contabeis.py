import zipfile
import pandas as pd
from pathlib import Path

# Caminhos dos arquivos
BASE_DIR = Path(__file__).resolve().parent.parent
RESOURCES_DIR = BASE_DIR / "resources"
ZIP_FILES = [RESOURCES_DIR / f"{n}T2023.zip" for n in range(1, 5)] + [RESOURCES_DIR / f"{n}T2024.zip" for n in range(1, 5)]
CSV_PATH_UNIFICADO = RESOURCES_DIR / 'demonstracoes_contabeis_unificado.csv'

# Lista de possíveis colunas que podem conter datas
POSSIVEIS_COLUNAS_DE_DATA = ["data", "data_registro", "data_contabil"]

# Lista de possíveis colunas numéricas
POSSIVEIS_COLUNAS_NUMERICAS = ["vl_saldo_inicial", "vl_saldo_final"]

def padronizar_datas(df):
    for coluna in POSSIVEIS_COLUNAS_DE_DATA:
        if coluna in df.columns:
            df[coluna] = pd.to_datetime(df[coluna], errors='coerce', dayfirst=True).dt.strftime('%Y-%m-%d')
    return df

def corrigir_numeros(df):
    """ Substitui vírgulas por pontos em colunas numéricas e converte para float. """
    for coluna in POSSIVEIS_COLUNAS_NUMERICAS:
        if coluna in df.columns:
            df[coluna] = df[coluna].astype(str).str.replace(',', '.').astype(float)
    return df

def extract_and_merge():
    dfs = []
    total_csvs = 0  # Contador de arquivos CSV processados

    for zip_path in ZIP_FILES:
        if not zip_path.exists():
            print(f"[AVISO] Arquivo ZIP não encontrado: {zip_path}")
            continue

        print(f"[INFO] Extraindo arquivos de {zip_path}...")

        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                csv_files = [f for f in zip_ref.namelist() if f.endswith('.csv')]

                if not csv_files:
                    print(f"[AVISO] Nenhum arquivo CSV encontrado em {zip_path}")
                    continue

                for file_name in csv_files:
                    with zip_ref.open(file_name) as csv_file:
                        try:
                            df = pd.read_csv(csv_file, sep=';', encoding='utf-8')
                            df.columns = df.columns.str.lower()  # Normaliza os nomes das colunas para minúsculas
                            df = padronizar_datas(df)  # Padroniza as datas para YYYY-MM-DD
                            df = corrigir_numeros(df)  # Corrige os valores numéricos
                            dfs.append(df)
                            total_csvs += 1
                            print(f"[SUCESSO] Arquivo {file_name} extraído com {len(df)} linhas.")
                        except Exception as e:
                            print(f"[ERRO] Falha ao ler {file_name} de {zip_path}: {e}")

        except zipfile.BadZipFile:
            print(f"[ERRO] Arquivo ZIP corrompido: {zip_path}")

    if dfs:
        merged_df = pd.concat(dfs, ignore_index=True)
        merged_df.to_csv(CSV_PATH_UNIFICADO, index=False, sep=';', encoding='utf-8')
        print(f"[SUCESSO] Arquivo CSV unificado salvo em {CSV_PATH_UNIFICADO} com {len(merged_df)} registros.")
    else:
        print("[FALHA] Nenhum dado foi extraído. Verifique os arquivos ZIP.")

if __name__ == "__main__":
    extract_and_merge()
