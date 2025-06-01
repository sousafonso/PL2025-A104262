import ply.lex as lex
import re

# Lista de tokens
tokens = [
    # Palavras-chave
    'PROGRAM', 'VAR', 'BEGIN', 'END', 'IF', 'THEN', 'ELSE',
    'WHILE', 'DO', 'FOR', 'TO', 'DOWNTO', 'FUNCTION', 'PROCEDURE',
    'INTEGER', 'BOOLEAN', 'CHAR', 'REAL', 'STRING', 'ARRAY', 'OF',
    'DIV', 'MOD', 'AND', 'OR', 'NOT', 'TRUE', 'FALSE',
    
    # Identificadores e literais
    'IDENTIFIER', 'INT_LIT', 'REAL_LIT', 'STRING_LIT', 'CHAR_LIT',
    
    # Operadores
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'ASSIGN', 'EQUAL', 'NOTEQUAL',
    'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL', 
    
    # Símbolos especiais
    'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
    'SEMICOLON', 'COLON', 'COMMA', 'DOT', 'DOTDOT'
]

# Expressões regulares para tokens simples
t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_ASSIGN = r':='
t_EQUAL = r'='
t_NOTEQUAL = r'<>'
t_LESSEQUAL = r'<='
t_GREATEREQUAL = r'>='
t_LESS = r'<'
t_GREATER = r'>'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_SEMICOLON = r';'
t_COLON = r':'
t_COMMA = r','
t_DOT = r'\.'
t_DOTDOT = r'\.\.'

# Ignorar espaços em branco e tabs
t_ignore = ' \t'

# Palavras reservadas (definidas antes de IDENTIFIER para maior precedência)
def t_PROGRAM(t):
    r'program'
    return t

def t_VAR(t):
    r'var'
    return t

def t_BEGIN(t):
    r'begin'
    return t

def t_END(t):
    r'end'
    return t

def t_IF(t):
    r'if'
    return t

def t_THEN(t):
    r'then'
    return t

def t_ELSE(t):
    r'else'
    return t

def t_WHILE(t):
    r'while'
    return t

def t_FOR(t):
    r'for'
    return t

def t_TO(t):
    r'to'
    return t

def t_DOWNTO(t):
    r'downto'
    return t

def t_DO(t):
    r'do'
    return t

def t_FUNCTION(t):
    r'function'
    return t

def t_PROCEDURE(t):
    r'procedure'
    return t

def t_INTEGER(t):
    r'integer'
    return t

def t_BOOLEAN(t):
    r'boolean'
    return t

def t_CHAR(t):
    r'char'
    return t

def t_REAL(t):
    r'real'
    return t

def t_STRING(t):
    r'string'
    return t

def t_ARRAY(t):
    r'array'
    return t

def t_OF(t):
    r'of'
    return t

def t_DIV(t):
    r'div'
    return t

def t_MOD(t):
    r'mod'
    return t

def t_AND(t):
    r'and'
    return t

def t_OR(t):
    r'or'
    return t

def t_NOT(t):
    r'not'
    return t

def t_TRUE(t):
    r'true'
    return t

def t_FALSE(t):
    r'false'
    return t

# Identificadores (deve vir APÓS as palavras reservadas)
def t_IDENTIFIER(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    return t

# Números (inteiros e reais)
def t_REAL_LIT(t):
    r'\d+\.\d+'
    t.value = float(t.value)
    return t

def t_INT_LIT(t):
    r'\d+'
    t.value = int(t.value)
    return t

# Caracteres entre aspas simples
def t_CHAR_LIT(t):
    r'\'[^\']\''
    t.value = t.value[1]  # Pega apenas o caractere
    return t

# Strings entre aspas simples
def t_STRING_LIT(t):
    r'\'[^\']*\''
    t.value = t.value[1:-1]  # Remove as aspas
    return t

# Comentários (entre { }, (* *) ou /* */)
def t_COMMENT_BLOCK(t):
    r'(\{[^}]*\})|(\(\*([^*]|\*+[^*)])*\*+\))'
    pass 

# Comentários começados por // (linha única)
def t_COMMENT_SINGLELINE(t):
    r'//[^\n]*'
    pass  

# Controle de linhas
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# Tratamento de erros
def t_error(t):
    print(f"Caractere ilegal '{t.value[0]}' na linha {t.lineno}")
    t.lexer.skip(1)

# Construir o lexer
lexer = lex.lex(reflags=re.IGNORECASE)

lexer.lineno = 1