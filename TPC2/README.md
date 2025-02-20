# Documentação da Solução

Esta solução foi implementada para resolver um TPC que tinha os seguintes objetivos:

- **Ler um dataset de obras musicais** a partir de um arquivo CSV (sem utilizar o módulo CSV do Python);
- **Gerar uma lista ordenada alfabeticamente dos compositores musicais**, eliminando duplicados;
- **Calcular a distribuição das obras por período**, ou seja, contar quantas obras estão catalogadas para cada período;
- **Construir um dicionário** que, para cada período, contenha uma lista ordenada alfabeticamente dos títulos das obras correspondentes.

## Implementação

1. **Leitura e Processamento do Arquivo CSV:**  
   O arquivo é lido linha a linha. A primeira linha, que contém o cabeçalho, é utilizada para identificar as colunas relevantes (como `nome`, `compositor` e `periodo`). As demais linhas são processadas somente se possuírem o número esperado de colunas, garantindo que dados incompletos ou linhas vazias sejam descartados.

2. **Lista de Compositores:**  
   Foi criado um conjunto com os compositores extraídos das linhas do CSV para evitar duplicados e, em seguida, esse conjunto foi ordenado alfabeticamente.

3. **Distribuição das Obras por Período:**  
   Para cada linha do dataset, o período da obra é utilizado como chave e num dicionário que contabiliza a quantidade de obras atribuídas a cada período.

4. **Obras por Período:**  
   Foi construído outro dicionário para mapear cada período numa lista contendo os títulos das obras. Após a agregação, as listas de títulos são ordenadas alfabeticamente.

5. **Exibição dos Resultados:**  
   Por fim, os resultados são exibidos na consola, mostrando a lista ordenada dos compositores, a distribuição das obras por período e, para cada período, os títulos das obras em ordem alfabética.

Esta implementação atende aos requisitos do TPC de forma simples e eficiente, utilizando apenas funcionalidades básicas do Python sem dependências externas para leitura de CSV.