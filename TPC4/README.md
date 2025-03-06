# Documentação do TPC4 – Analisador Léxico para Linguagem de Query

## Objetivo

Neste TPC, o objetivo é construir um analisador léxico utilizando a biblioteca PLY (Python Lex-Yacc) para interpretar uma linguagem de query inspirada na DBpedia. 

## O que é Implementado

1. **Definição de Tokens:**  
   São definidos diversos tokens para identificar:
   - Palavras-chave como `SELECT`, `WHERE` e `LIMIT`;
   - O token `a` para a relação;
   - Variáveis, que iniciam com `?`;
   - URIs no formato, por exemplo, `dbo:MusicalArtist`;
   - Strings, no formato `"texto"@en`;
   - Números e símbolos como `{`, `}`, e `.`;
   - Comentários (iniciados por `#`).

2. **Expressões Regulares:**  
   Cada token é definido utilizando uma expressão regular. Isto permite extrair corretamente os campos e respeitar as particularidades, como aspas duplas nas strings.

3. **Tratamento de Espaços, Comentários e Erros:**  
   O lexer ignora espaços e tabulações e trata comentários corretamente. Caso sejam encontrados caracteres ilegais, o analisador reporta o erro e continua a sua execução.

4. **Teste do Lexer:**  
   O ficheiro `TPC4.py` contém um exemplo prático onde o input (uma query real) é alimentado no lexer, e os tokens extraídos são impressos no terminal, permitindo verificar o funcionamento do analisador léxico.

## Considerações Finais

Esta implementação demonstra a utilização prática da biblioteca PLY para construir um analisador léxico. O resultado obtido facilita a posterior análise sintática e a execução de queries numa linguagem específica, servindo como base para sistemas mais complexos de processamento de linguagem.

## Autoria

- **Nome:** Afonso Sousa
- **ID:** A104262