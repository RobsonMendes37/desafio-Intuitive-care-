-- Query para pegar as 10 operadoras com maiores despesas no último trimestre
SELECT 
    dc.reg_ans,
    descricao,
	oa.razao_social AS nome_operadora,
    SUM(vl_saldo_final - vl_saldo_inicial) AS total_despesa 
FROM demonstracoes_contabeis dc
JOIN operadoras_ativas oa ON dc.reg_ans = oa.registro_ans
WHERE descricao = 'EVENTOS/ SINISTROS CONHECIDOS OU AVISADOS  DE ASSISTÊNCIA A SAÚDE MEDICO HOSPITALAR '
 AND data >= '2024-09-01'
GROUP BY dc.reg_ans, descricao, nome_operadora
ORDER BY total_despesa DESC
LIMIT 10;
