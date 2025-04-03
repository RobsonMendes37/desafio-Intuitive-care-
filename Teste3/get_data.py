import os
import requests
import time

def baixar_zips(urls, tentativas=3):
    pasta = "Teste3/resources"
    os.makedirs(pasta, exist_ok=True)
    
    for url in urls:
        nome_arquivo = os.path.join(pasta, url.split("/")[-1])
        print(f"Baixando {url}...")

        for tentativa in range(1, tentativas + 1):
            try:
                resposta = requests.get(url, stream=True, timeout=10)
                resposta.raise_for_status()  # Levanta um erro se a resposta for ruim (ex: 404, 500)
                
                with open(nome_arquivo, "wb") as arquivo:
                    for chunk in resposta.iter_content(chunk_size=1024):
                        arquivo.write(chunk)
                
                print(f"Arquivo salvo: {nome_arquivo}")
                break  # Sai do loop se o download for bem-sucedido
            
            except requests.exceptions.RequestException as e:
                print(f"Erro ao baixar {url} (tentativa {tentativa}/{tentativas}): {e}")
                if tentativa < tentativas:
                    time.sleep(5)  # Aguarda 5 segundos antes de tentar novamente
                else:
                    print(f"Falha ao baixar {url} após {tentativas} tentativas.")

urls = [ #dados 2023
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/1T2023.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/2T2023.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/3T2023.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2023/4T2023.zip",

        #dados 2024
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/1T2024.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/2T2024.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/3T2024.zip",
    "https://dadosabertos.ans.gov.br/FTP/PDA/demonstracoes_contabeis/2024/4T2024.zip",

        #dados cadastrais
    "https://dadosabertos.ans.gov.br/FTP/PDA/operadoras_de_plano_de_saude_ativas/Relatorio_cadop.csv"

]

baixar_zips(urls)
