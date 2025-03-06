# Conversor de Markdown para HTML

Este projeto consiste em criar um conversor de Markdown para HTML que suporta os seguintes elementos:

1. **Cabeçalhos** (`#`, `##`, `###`)
2. **Negrito** (`**texto**`)
3. **Itálico** (`*texto*`)
4. **Listas numeradas** (`1. item`)
5. **Links** (`[texto](url)`)
6. **Imagens** (`![texto](url)`)

Abaixo, explicamos o problema, os métodos utilizados e a solução implementada.

---

## Problema

O objetivo é converter texto em Markdown para HTML, seguindo as regras básicas da sintaxe Markdown. Para isso, precisamos identificar padrões no texto (como `#`, `**`, `*`, `1.`, `[texto](url)`, etc.) e substituí-los pelas tags HTML correspondentes.

---

## Métodos Utilizados

### 1. **Expressões Regulares (Regex)**
   - As expressões regulares são usadas para identificar padrões no texto.
   - Exemplos de padrões:
     - Cabeçalhos: `^#\s+(.*)`
     - Negrito: `\*\*(.*?)\*\*`
     - Itálico: `\*(.*?)\*`
     - Listas numeradas: `^(\d+)\.\s+(.*)`
     - Links: `\[(.*?)\]\((.*?)\)`
     - Imagens: `!\[(.*?)\]\((.*?)\)`

### 2. **Substituição de Texto**
   - Após identificar os padrões, usamos a função `re.sub()` para substituir os padrões pelas tags HTML correspondentes.
   - Exemplo:
     ```python
     re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', texto)
     ```

### 3. **Captura de Grupos**
   - Usamos parênteses `()` para definir grupos de captura.
   - Os grupos capturados são referenciados usando `\1`, `\2`, etc.
   - Exemplo:
     - Regex: `^#\s+(.*)`
     - Substituição: `<h1>\1</h1>`

---

## Solução Implementada

### 1. **Cabeçalhos**
   - Regex: `^#\s+(.*)`
   - Substituição: `<h1>\1</h1>`
   - Exemplo:
     - Entrada: `# Título`
     - Saída: `<h1>Título</h1>`

### 2. **Negrito**
   - Regex: `\*\*(.*?)\*\*`
   - Substituição: `<b>\1</b>`
   - Exemplo:
     - Entrada: `**negrito**`
     - Saída: `<b>negrito</b>`

### 3. **Itálico**
   - Regex: `\*(.*?)\*`
   - Substituição: `<i>\1</i>`
   - Exemplo:
     - Entrada: `*itálico*`
     - Saída: `<i>itálico</i>`

### 4. **Listas Numeradas**
   - Regex: `^(\d+)\.\s+(.*)`
   - Substituição: `<li>\2</li>`
   - Exemplo:
     - Entrada:
       ```
       1. Primeiro item
       2. Segundo item
       ```
     - Saída:
       ```html
       <ol>
       <li>Primeiro item</li>
       <li>Segundo item</li>
       </ol>
       ```

### 5. **Links**
   - Regex: `\[(.*?)\]\((.*?)\)`
   - Substituição: `<a href="\2">\1</a>`
   - Exemplo:
     - Entrada: `[página da UC](http://www.uc.pt)`
     - Saída: `<a href="http://www.uc.pt">página da UC</a>`

### 6. **Imagens**
   - Regex: `!\[(.*?)\]\((.*?)\)`
   - Substituição: `<img src="\2" alt="\1"/>`
   - Exemplo:
     - Entrada: `![imagem](http://exemplo.com)`
     - Saída: `<img src="http://exemplo.com" alt="imagem"/>`

## Autoria

- **Nome:** Afonso Sousa
- **ID:** A104262