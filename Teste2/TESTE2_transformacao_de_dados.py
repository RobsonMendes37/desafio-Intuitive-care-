import pdfplumber
import pandas as pd
import zipfile

pdf_file = "Teste2/Anexo_I.pdf"
csv_file = "Teste2/Rol_de_Procedimentos.csv"
zip_file = "Teste2/Teste_FranciscoRobsonQueirozMendes.zip"  

substituicoes = {
    "OD": "Procedimentos Odontológicos",
    "AMB": "Procedimentos Ambulatoriais"
}

# Lista para armazenar as tabelas 
tabelas = []

with pdfplumber.open(pdf_file) as pdf:
    for page in pdf.pages:
        
        tabela = page.extract_table()
        if tabela:
            tabelas.extend(tabela)  # Adiciona a tabela extraída à lista

# Converte a tabela para um DataFrame pandas
df = pd.DataFrame(tabelas)

# Define a primeira linha como cabeçalho (se necessário)
df.columns = df.iloc[0] 
df = df[1:]  

df.replace(substituicoes, inplace=True)

# Salva os dados em um arquivo CSV
df.to_csv(csv_file, index=False, encoding="utf-8")

# Compacta o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_file, "w", zipfile.ZIP_DEFLATED) as zipf:
    zipf.write(csv_file)

print(f"Processo concluido! O arquivo {zip_file} foi criado com sucesso.")
