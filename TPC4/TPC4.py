import ply.lex as lex

# Lista de tokens
tokens = (
    'SELECT',
    'WHERE',
    'LIMIT',
    'A',
    'VARIABLE',
    'URI',
    'STRING',
    'NUMBER',
    'LBRACE',
    'RBRACE',
    'DOT',
    'COMMENT',
)

# Expressões regulares para tokens simples
t_SELECT = r'SELECT'
t_WHERE = r'WHERE'
t_LIMIT = r'LIMIT'
t_A = r'a'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_DOT = r'\.'
t_ignore = ' \t'  # Ignorar espaços e tabs

# Expressão regular para variáveis (começam com ?)
def t_VARIABLE(t):
    r'\?[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Expressão regular para URIs (ex: dbo:MusicalArtist)
def t_URI(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*:[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Expressão regular para strings (ex: "Chuck Berry"@en)
def t_STRING(t):
    r'"[^"]+"@[a-z]+'
    return t

# Expressão regular para números (ex: 1000)
def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)  # Converter para inteiro
    return t

# Expressão regular para comentários (começam com #)
def t_COMMENT(t):
    r'\#.*'
    return t

# Controle de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal: '{t.value[0]}'")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex()

# Testar o lexer
data = """
# DBPedia: obras de Chuck Berry
select ?nome ?desc where {
?s a dbo:MusicalArtist.
?s foaf:name "Chuck Berry"@en .
?w dbo:artist ?s.
?w foaf:name ?nome.
?w dbo:abstract ?desc
} LIMIT 1000
"""

# Alimentar o lexer com os dados
lexer.input(data)

# Imprimir os tokens encontrados
for token in lexer:
    print(token)