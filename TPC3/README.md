#Conversor de Markdown para HTML#
Este projeto consiste em criar um conversor de Markdown para HTML que suporta os seguintes elementos:

Cabeçalhos (#, ##, ###)
Negrito (**texto**)
Itálico (*texto*)
Listas numeradas (1. item)
Links ([texto](url))
Imagens (![texto](url))
Abaixo, explicamos o problema, os métodos utilizados e a solução implementada.

##Problema##

O objetivo é converter texto em Markdown para HTML, seguindo as regras básicas da sintaxe Markdown. Para isso, precisamos identificar padrões no texto (como #, **, *, 1., [texto](url), etc.) e substituí-los pelas tags HTML correspondentes.

##Métodos Utilizados##

1. Expressões Regulares (Regex)

As expressões regulares são usadas para identificar padrões no texto.
Exemplos de padrões:
Cabeçalhos: ^#\s+(.*)
Negrito: \*\*(.*?)\*\*
Itálico: \*(.*?)\*
Listas numeradas: ^(\d+)\.\s+(.*)
Links: \[(.*?)\]\((.*?)\)
Imagens: !\[(.*?)\]\((.*?)\)
2. Substituição de Texto

Após identificar os padrões, usamos a função re.sub() para substituir os padrões pelas tags HTML correspondentes.
Exemplo:

re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)

3. Captura de Grupos

Usamos parênteses () para definir grupos de captura.
Os grupos capturados são referenciados usando \1, \2, etc.
Exemplo:
Regex: ^#\s+(.*)
Substituição: <h1>\1</h1>

##Solução Implementada##

1. Cabeçalhos

Regex: ^#\s+(.*)
Substituição: <h1>\1</h1>

2. Negrito

Regex: \*\*(.*?)\*\*
Substituição: <b>\1</b>

3. Itálico

Regex: \*(.*?)\*
Substituição: <i>\1</i>

4. Listas Numeradas

Regex: ^(\d+)\.\s+(.*)
Substituição: <li>\2</li>

5. Links

Regex: \[(.*?)\]\((.*?)\)
Substituição: <a href="\2">\1</a>

6. Imagens

Regex: !\[(.*?)\]\((.*?)\)
Substituição: <img src="\2" alt="\1"/>