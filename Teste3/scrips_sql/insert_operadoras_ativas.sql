-- depois de criar a tabela e importar os dados do CSV pelo psql, troque o caminho do arquivo para ser referenciado no seu computador
\copy operadoras_ativas (registro_ans, cnpj, razao_social, nome_fantasia, modalidade, logradouro, numero, complemento, bairro, cidade, uf, cep, ddd, telefone, fax, endereco_eletronico, representante, cargo_representante, regiao_de_comercializacao, data_registro_ans)
FROM 'C:/Users/robso/Documents/desafio-intuitive-care/Teste3/resources/Relatorio_cadop.csv' 
DELIMITER ';' CSV HEADER ENCODING 'UTF8';
