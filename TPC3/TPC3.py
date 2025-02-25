import re

def conversor (markdown):

    # Codificação dos #'s
    markdown = re.sub(r'^#\s+(.*)?', r'<h1>\1</h1', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^##\s+(.*)?', r'<h2>\1</h2', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'^###\s+(.*)?', r'<h3>\1</h3', markdown, flags=re.MULTILINE)

    # Codificação do Negrito
    markdown = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', markdown)

    #Codificação do Itálico
    markdown = re.sub(r'\*(.*?)\*', r'<i>\1</i>', markdown)

    #Codificação das listas
    markdown = re.sub(r'^(\d+)\.\s+(.*)$', r'<li>\2</li>', markdown, flags=re.MULTILINE)
    markdown = re.sub(r'(<li>.*</li>)', r'<ol>\n\1\n</ol>', markdown, flags=re.DOTALL)

    #Codificação de links
    markdown = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', markdown)

    #Codificação de Imagens
    markdown = re.sub(r'!\[(.*?)\]\((.*?)\)', r'<img src="\2" alt="\1"/>', markdown)

    return markdown

    # Exemplo de uso
markdown_text = """
# Exemplo de cabeçalho

Este é um **exemplo** de texto em negrito e *itálico*.

1. Primeiro item
2. Segundo item
3. Terceiro item

Como pode ser consultado em [página da UC](http://www.uc.pt).

Como se vê na imagem seguinte: ![imagem dum coelho](http://www.coellho.com).
"""

html_output = conversor(markdown_text)
print(html_output)