from Teste3.app import insert_demonstracoes_contabeis, insert_operadoras_ativas
from Teste3.app.merge_demonstracoes_contabeis import extract_and_merge

print("Iniciando processamento...")
extract_and_merge()
insert_demonstracoes_contabeis()
insert_operadoras_ativas()
print("Processamento concluído.")

