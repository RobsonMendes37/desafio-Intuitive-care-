
-- despois de criar a tabela e importar os dados do CSV pelo psql, troque o caminho do arquivo para ser referenciado no seu computador
\copy demonstracoes_contabeis (data, reg_ans, cd_conta_contabil, descricao, vl_saldo_inicial, vl_saldo_final) 
FROM 'C:/Users/robso/Documents/desafio-intuitive-care/Teste3/resources/demonstracoes_contabeis_unificado.csv' 
DELIMITER ';' CSV HEADER ENCODING 'UTF8';
