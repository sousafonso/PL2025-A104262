import ply.lex as lex
import ply.yacc as yacc
from tokenizer import tokens
from symbol_table import SymbolTable, symbol_table
from node import *

parse_error_occurred = False
precedence = (
    ('left', 'OR'),
    ('left', 'AND'),
    ('left', 'EQUAL', 'NOTEQUAL'),
    ('left', 'LESS', 'LESSEQUAL', 'GREATER', 'GREATEREQUAL'),
    ('left', 'PLUS', 'MINUS'),
    ('left', 'TIMES', 'DIV', 'DIVIDE', 'MOD'),
    ('nonassoc', 'ELSE')
)

def p_program(p):
    """ program : PROGRAM IDENTIFIER SEMICOLON vars command_list DOT"""
    
    p[0] = Program(p[2], p[5])

def p_vars(p):
    """ vars : VAR var_declarations"""
    p[0] = p[2]


def p_vars_empty(p):
    """ vars : empty """
    p[0] = None

def p_var_declarations(p):
    """ var_declarations : var_declarations var_declaration
                        | var_declaration """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[2]]

def p_var_declaration(p):
    """ var_declaration : identifiers_list COLON type SEMICOLON """
    symbol_table.add(p[1], p[3])

    p[0] = None

def p_identifiers_list(p):
    """ identifiers_list : identifiers_list COMMA IDENTIFIER
                        | IDENTIFIER """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_type(p):
    """ type : simple_type
            | array_type """
    p[0] = p[1]
    
def p_simple_type(p):
    """ simple_type : INTEGER
                    | REAL
                    | STRING
                    | CHAR
                    | BOOLEAN """
    p[0] = p[1]

def p_array_type(p):
    """ array_type : ARRAY LBRACKET range RBRACKET OF simple_type """
    p[0] = {'type': 'array', 'base_type': p[6], 'range': p[3]}

def p_range(p):
    """ range : INT_LIT DOTDOT INT_LIT """
    # Armazena o intervalo como uma tupla (início, fim)
    p[0] = (p[1], p[3])


def p_command_list(p):
    """command_list : BEGIN command_list_opt END
                    | command"""
    if len(p) == 2:  # Single command scenario outside BEGIN/END
        p[0] = [p[1]]
    else:
        p[0] = p[2]

def p_command_list_opt(p):
    """command_list_opt : command_list_body
                        | command_list_body SEMICOLON"""
    # Both alternatives yield the same list of commands.
    p[0] = p[1]

def p_command_list_body(p):
    """command_list_body : command_list_body SEMICOLON command
                         | command"""
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1] + [p[3]]

def p_command(p):
    """command : function_call
               | assignment
               | if
               | while
               | for"""
    p[0] = p[1]

def p_function_call(p):
    """
    function_call : IDENTIFIER LPAREN args_list RPAREN
    """
    func = p[1].lower()
    p[0] = FunctionCall(func, p[3])
    

    

def p_args_list(p):
    """
    args_list : args_list COMMA expressionBool
               | expressionBool
               | empty
    """
    if len(p) == 2:
        p[0] = [p[1]]
    elif len(p) == 4:
        p[0] = p[1] + [p[3]]
    else:
        p[0] = []


# Dividir em const e var, var precisa de acomodar arrays
def p_argument(p):
    """argument : literal
                | var
    """
    p[0] = p[1]
    
def p_literal(p):
    """literal : STRING_LIT
            | CHAR_LIT
            | INT_LIT
            | REAL_LIT
            | TRUE
            | FALSE
    """
    if p.slice[1].type == 'STRING_LIT':
        p[0] = Literal("string", p[1])
        # p[0] = String

    elif p.slice[1].type == 'INT_LIT':
        value = p[1]    
        p[0] = Literal("integer", int(value))

    elif p.slice[1].type == 'REAL_LIT':
        value = p[1]    
        p[0] = Literal("real", float(value))

    elif p.slice[1].type == 'TRUE':
        p[0] = Literal("boolean", True)

    elif p.slice[1].type == 'FALSE':
        p[0] = Literal("boolean", False)

    elif p.slice[1].type == 'CHAR_LIT':
        value = p[1]    
        p[0] = Literal("char", value)

def p_var(p):
    """var : IDENTIFIER
            | IDENTIFIER LBRACKET expression RBRACKET
    """
    var_info = symbol_table.symbols.get(p[1])
    if var_info is None:
        raise Exception(f"Variável '{p[1]}' não declarada.")
    try:
        # Se é um acesso a array (com índice)
        if len(p) == 5:
            if var_info[0] == 'string':
                p[0] = Array(Identifier(p[1]), p[3])
                
            # Verificar se a variável é realmente um array
            elif not isinstance(var_info[0], dict) or var_info[0].get('type') != 'array':
                raise Exception(f"Variável '{p[1]}' não é um array.")
            p[0] = Array(Identifier(p[1]), p[3])
            # Definir o tipo com base no tipo base do array
            # p[0].type = var_info[0].get('base_type')
        else:
            # Acesso normal a variável
            p[0] = Identifier(p[1])
    except Exception as e:
        line_num = p.lexer.lineno
        line_text = p.lexer.lexdata.splitlines()[line_num - 1]
        print(f"Error at line {line_num}: {e}")
        print(line_text)
        global parse_error_occurred
        parse_error_occurred = True



def p_if(p): 
    """
    if : IF expressionBool THEN command_list else
    """
    p[0] = If(p[2], p[4], p[5])

def p_else(p):
    """
    else : ELSE command_list
         | empty
    """
    if len(p) == 3:
        p[0] = p[2]
    else:
        p[0] = None


def p_while(p):
    """
    while : WHILE expressionBool DO command_list"""
    p[0] = While(p[2], p[4])


def p_for(p):
    """
    for : FOR IDENTIFIER ASSIGN expression to_or_downto expression DO command_list
    """
    p[0] = For(Identifier(p[2]), p[4], p[5], p[6], p[8])

def p_to_or_downto(p):
    """
    to_or_downto : TO
                 | DOWNTO
    """
    p[0] = p[1]

def p_expressionBool(p):
    """expressionBool : expression 
                  | expression opRel expression
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        try:
            p[0] = BinaryOp(p[2], p[1], p[3])
        except Exception as e:
            line_num = p.lexer.lineno
            line_text = p.lexer.lexdata.splitlines()[line_num - 1]
            print(f"Error at line {line_num}: {e}")
            print(line_text)
            global parse_error_occurred
            parse_error_occurred = True

def p_opRel(p):
    """opRel : EQUAL
            | NOTEQUAL
            | LESS
            | LESSEQUAL
            | GREATER
            | GREATEREQUAL
    """
    p[0] = p[1]

def p_expression(p):
    """expression : term
                | expression opAd term"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        try:
            p[0] = BinaryOp(p[2], p[1], p[3])
        except Exception as e:
            line_num = p.lexer.lineno
            line_text = p.lexer.lexdata.splitlines()[line_num - 1]
            print(f"Error at line {line_num}: {e}")
            print(line_text)
            global parse_error_occurred
            parse_error_occurred = True

def p_term(p):
    """term : factor
            | term opMul factor"""
    if len(p) == 2:
        p[0] = p[1]
    else:
        try:
            p[0] = BinaryOp(p[2], p[1], p[3])
        except Exception as e:
            line_num = p.lexer.lineno
            line_text = p.lexer.lexdata.splitlines()[line_num - 1]
            print(f"Error at line {line_num}: {e}")
            print(line_text)
            global parse_error_occurred
            parse_error_occurred = True


def p_opAd(p):
    """opAd : PLUS
            | MINUS
            | AND"""
    p[0] = p[1]

def p_opMul(p):
    """opMul : TIMES
            | DIVIDE
            | DIV
            | MOD
            | OR"""
    p[0] = p[1]


def p_factor(p):
    """factor : argument
                | LPAREN expressionBool RPAREN
                | function_call
    """
    if len(p) == 2:
        p[0] = p[1]
    else: 
        p[0] = p[2]
    

def p_assignment(p):
    """
    assignment : IDENTIFIER ASSIGN expression
               | IDENTIFIER LBRACKET expression RBRACKET ASSIGN expression
    """
    try:
        if len(p) == 4:
            # Atribuição a variável simples
            p[0] = Assignment(Identifier(p[1]), p[3])
        else:
            # Atribuição a elemento de array
            p[0] = Assignment(Array(Identifier(p[1]), p[3]), p[6])
    except Exception as e:
        line_num = p.lexer.lineno
        line_text = p.lexer.lexdata.splitlines()[line_num - 1]
        print(f"Error at line {line_num}: {e}")
        print(line_text)
        global parse_error_occurred
        parse_error_occurred = True

def p_empty(p):
    """ empty : """
    pass

def p_error(p):
    if p:
        data = p.lexer.lexdata
        lines = data.splitlines()
        if p.lineno <= len(lines):
            error_line = lines[p.lineno - 1]
        else:
            error_line = "<unknown line>"
        
        print(f"Syntax error at line {p.lineno}, near '{p.value}'")
        print(error_line)
        
        line_start = data.rfind('\n', 0, p.lexpos) + 1
        pos_in_line = p.lexpos - line_start
        
        print(" " * pos_in_line + "^")
    else:
        print("Syntax error at EOF")

parser = yacc.yacc()