-- Criar a tabela se não existir
CREATE TABLE IF NOT EXISTS demonstracoes_contabeis (
    id SERIAL PRIMARY KEY,
    data DATE NOT NULL,
    reg_ans VARCHAR(255) NOT NULL,
    cd_conta_contabil VARCHAR(255) NOT NULL,
    descricao VARCHAR(255) NOT NULL,
    vl_saldo_inicial NUMERIC NOT NULL,
    vl_saldo_final NUMERIC NOT NULL
);