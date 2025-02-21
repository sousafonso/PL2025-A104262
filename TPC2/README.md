# Documentação da Solução

Esta solução foi desenvolvida para resolver um TPC que tinha os seguintes objectivos:

- **Ler um conjunto de obras musicais** a partir de um ficheiro CSV (sem utilizar o módulo CSV do Python);
- **Gerar uma lista ordenada alfabeticamente dos compositores musicais**, eliminando duplicados;
- **Calcular a distribuição das obras por período**, ou seja, contar o número de obras catalogadas para cada período;
- **Construir um dicionário** que, para cada período, contenha uma lista ordenada alfabeticamente dos títulos das obras correspondentes.

## Implementação

1. **Leitura e Processamento do Ficheiro CSV:**  
   O ficheiro é lido linha a linha e processado utilizando uma expressão regular para extrair os campos relevantes. O padrão utilizado é:
   r'([^;]+);("(?:[^"](?:"[^"]))"|[^;]+);([^;]+);([^;]+);([^;]+);([^;])\n?'


Este regex captura:
- O primeiro campo (nome da obra);
- O segundo campo, que pode estar entre aspas (permitindo a presença de aspas duplas escapadas) ou não;
- Campos adicionais correspondentes aos restantes dados, como o ano de criação, o período, o compositor, etc.

Esta abordagem garante que os dados sejam extraídos correctamente, mesmo que alguns campos contenham o delimitador `;` ou aspas internas.

2. **Lista de Compositores:**  
Utilizou-se um conjunto para armazenar os compositores extraídos das linhas do CSV, evitando duplicados. Posteriormente, o conjunto foi ordenado alfabeticamente para formar a lista final.

3. **Distribuição das Obras por Período:**  
Cada linha do conjunto de dados é processada para identificar o período da obra. Foi utilizado um dicionário que contabiliza o número de obras para cada período.

4. **Obras por Período:**  
Outro dicionário mapeia cada período para uma lista dos títulos das obras. Após a agregação, estas listas são ordenadas alfabeticamente.

5. **Exibição dos Resultados:**  
Os resultados são gravados num ficheiro de saída (`outputs.txt`) e também apresentados no terminal, seguindo o seguinte formato:

- Lista ordenada dos compositores;
- Distribuição das obras por período;
- Dicionário com os títulos das obras por período (ordenados alfabeticamente).

Esta implementação satisfaz os requisitos do TPC de forma simples, robusta e eficiente, utilizando expressões regulares para o processamento do CSV sem dependências externas.