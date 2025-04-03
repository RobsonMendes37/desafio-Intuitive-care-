import pdfplumber
import pandas as pd
import zipfile

# Nome do arquivo PDF (supondo que já foi baixado no teste anterior)
pdf_file = "Anexo_I.pdf"
csv_file = "Rol_de_Procedimentos.csv"
zip_file = "Teste_FranciscoRobsonQueirozMendees.zip"  # Substitua "SeuNome" pelo seu nome

# Dicionário para substituir abreviações
substituicoes = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

# Lista para armazenar todas as tabelas extraídas
tabelas = []

# Abre o PDF e percorre todas as páginas
with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        # Tenta extrair a tabela da página
        tabela = page.extract_table()
        if tabela:
            tabelas.extend(tabela)  # Adiciona a tabela extraída à lista

# Converte a tabela para um DataFrame pandas
df = pd.DataFrame(tabelas)

# Define a primeira linha como cabeçalho (se necessário)
df.columns = df.iloc[0]  # Usa a primeira linha como cabeçalho
df = df[1:]  # Remove a linha duplicada do cabeçalho

# Substitui as abreviações conforme a legenda
df.replace(substituicoes, inplace=True)

# Salva os dados em um arquivo CSV
df.to_csv(csv_file, index=False, encoding="utf-8")

# Compacta o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file)

print(f"Processo concluído! O arquivo {zip_file} foi criado com sucesso.")
