# SERS-GS2

Integrantes
Guilherme Marques dos Santos RM573112
Gustavo Naville Tobara RM570674
Pedro Henrique Silva Santos RM571537

Descrição do publico
Publico classe media da cidade de São Paulo preocupado com a alta conta de luz.

Funcionalidades de energia
O assistente funciona por um menu no terminal:
Calcula o consumo dos aparelhos (kWh/mês e R$/mês) usando energia = potência x tempo.
Compara duas alternativas para os mesmos 10 anos: trocar lâmpadas por LED  e energia solar . Mostra investimento, economia por mês, retorno, saldo em 10 anos e CO2 evitado.
Uma IA explica os resultados em linguagem simples. O Python faz as contas e a IA só explica, sem inventar números.

Dados e premissas
Tarifa R$  0,7894/kWh - ANEEL
fator de CO2 0,04 kg/kWh - MCTI
4,5 horas de sol por dia 
rendimento do sistema solar 0,80 - estimado
custo solar R$ 4.500/kWp - 
taxa mínima da conta 50 kWh
LED de 9 W a R$ 4. - Lâmpada Led Ourolux 9W Bivolt 6500K
Aparelhos de exemplo estimados.

Cálculos
kWh por mês = potência (W) x horas por dia x 30 / 1000
Custo = kWh x tarifa
kWp solar = (consumo - taxa mínima) / (horas de sol x 30 x rendimento)
Payback = investimento / (economia por mês x 12)
Saldo em 10 anos = economia por mês x 12 x 10 - investimento
CO2 evitado = kWh economizados x 12 x 10 x fator de CO2

Resultados do exemplo
Consumo total: 358,8 kWh/mês, cerca de R$ 283,24. 
Alternativa A (LED): investimento R$ 20,00; economia R$ 30,19/mês; payback 0,1 ano; saldo em 10 anos R$ 3.603,35; CO2 evitado 340 kg.
Alternativa B (solar): investimento R$ 12.866,67; economia R$ 243,77/mês; payback 4,4 anos; saldo em 10 anos R$ 16.385,34; CO2 evitado 2.742 kg.

Recomendação
A solar economiza mais, mas exige investimento alto e telhado adequado. O CO2 evitado é pequeno porque a rede elétrica brasileira já é majoritariamente renovável. Dito isso, avaliar se o custo para montar a solar cabe dentro do orçamento.

Limitações
Os valores são estimativas, não garantias. A tarifa muda, a solar depende do telhado e não foram considerados manutenção.
