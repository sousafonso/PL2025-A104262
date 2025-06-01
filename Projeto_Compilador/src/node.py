from symbol_table import symbol_table
import operator


class Node():
    def __init__(self):
        pass

    def generate(self):
        pass

class Program(Node):
    def __init__(self, name, commands):
        self.name = name
        self.commands = commands

    def initialize_arrays(self):
        code = ""
        # Para cada símbolo na tabela, verifique se é um array
        for var_name, symbol in symbol_table.symbols.items():
            if isinstance(symbol[0], dict) and symbol[0].get('type') == 'array':
                array_size = symbol[2]  # Tamanho do array
                pos = symbol[1]         # Posição na pilha
                
                # Alocar espaço para o array
                code += f"PUSHI {array_size}\nALLOCN\n"
                
                # Armazenar o ponteiro para o array na variável
                code += f"STOREG {pos}\n"
        
        return code
        
    def generate(self):
        # Inicializar arrays
        result = self.initialize_arrays()
        
        # Gerar código para os comandos
        cmds = self.commands if isinstance(self.commands, list) else [self.commands]
        for command in cmds:
            generated = command.generate()
            #generated = generated.replace("\r", "")
            result += generated
        
        return result  #.replace("\r", "").replace("\n\n", "\n")


class FunctionCall(Node):
    def __init__(self, name, args):
        self.name = name.upper()
        self.args = args if isinstance(args, list) else [args]

    def generate(self):
        result = ""
        if self.name.lower() == "write":
            if len(self.args) == 1:
                result = self.args[0].generate()
                if self.args[0].type == "string":
                    result += "WRITES\n"
                elif self.args[0].type == "integer":
                    result += "WRITEI\n"
                elif self.args[0].type == "real":
                    result += "WRITEF\n"
                elif self.args[0].type == "boolean":
                    result += "WRITEI\n"
                elif self.args[0].type == "char":
                    result += "WRITECHR\n"
                
            else:
                result = self.concat() + "WRITES\n"

        elif self.name.lower() == "writeln":
            if len(self.args) == 1:
                result = self.args[0].generate()
                if self.args[0].type == "string":
                    result += "WRITES\n"
                elif self.args[0].type == "integer":
                    result += "WRITEI\n"
                elif self.args[0].type == "real":
                    result += "WRITEF\n"
                elif self.args[0].type == "boolean":
                    result += "WRITEI\n"
                elif self.args[0].type == "char":
                    result += "WRITECHR\n"
                    
            else:
                result = self.concat() + "WRITES\n"
            result += "WRITELN\n"

        elif self.name.lower() == "readln":
            for arg in self.args:
                read_str = ""
                read_str += "READ\n"
                if arg.type.lower() == "integer":
                    read_str += "ATOI\n"
                elif arg.type.lower() == "real":
                    read_str += "ATOF\n"
                elif arg.type.lower() == "char":
                    read_str += "CHRCODE\n"
                elif isinstance(arg, Array):
                    if arg.type.lower() == "integer":
                        read_str += "ATOI\n"
                    elif arg.type.lower() == "real":
                        read_str += "ATOF\n"
                
                # Se for um identificador simples
                if hasattr(arg, "name"):
                    result += read_str + f"STOREG {symbol_table.get_stack_pos(arg.name)}\n"
                # Se for acesso a array, usa o atributo identifier
                elif isinstance(arg, Array):
                    
                    # Depois calculamos o endereço do elemento no array
                    pos = symbol_table.get_stack_pos(arg.identifier.name)
                    
                    # Agora calculamos o endereço
                    result += f"PUSHG {pos}\n"  # Carrega o ponteiro para o array
                    result += arg.index.generate()  # Calcula o índice

                    sym = symbol_table.symbols.get(arg.identifier.name)
                    if isinstance(sym[0], dict) and sym[0].get('range'):
                        min_index = sym[0]['range'][0]
                        if min_index > 0:
                            result += f"PUSHI {min_index}\nSUB\n"
                    result += read_str
                    # Ajustar se o array começa em índice diferente de 0
                    # Armazena o valor no array - a ordem é: valor, endereço, STOREN
                    result += "STOREN\n"
        
        elif self.name.lower() == "length":
            if len(self.args) == 1:
                if self.args[0].type == "string":
                    result += self.args[0].generate()
                    result += "STRLEN\n"
                    self.type = "integer"
                else:
                    raise Exception("Length function only accepts strings")
            
        return result

    def concat(self):
        reversed_args = list(reversed(self.args))
        result = reversed_args[0].generatestr()
        for arg in reversed_args[1:]:
            result += arg.generatestr() + "CONCAT\n"
        return result
            
# :=
class Assignment(Node):
    def __init__(self, target, value):
        self.target = target
        self.value = value

    def generate(self):

        result = self.value.generate()
        
        if self.target.type == "array":
            symbol = symbol_table.symbols.get(self.target.identifier.name)
            pos = symbol[1]  # Posição do ponteiro do array
            
            # Carregar o ponteiro do array
            addr_code = f"PUSHG {pos}\n"
            
            # Calcular o índice
            addr_code += self.target.index.generate()
            
            # Ajustar o índice se o array começa em um valor diferente de 0
            if isinstance(symbol[0], dict) and symbol[0].get('range'):
                min_index = symbol[0]['range'][0]
                if min_index > 0:
                    addr_code += f"PUSHI {min_index}\nSUB\n"
                        
            # Verificar compatibilidade de tipos
            if self.target.type == self.value.type:
                return  addr_code + result + "STOREN\n"
            elif self.target.type.lower() == "real" and self.value.type.lower() == "integer":
                return result + "ITOF\n" + addr_code + "STOREN\n"
            else:
                raise Exception(f"Cannot assign {self.value.type} to array element of type {self.target.type}")
        
        # Atribuição a variável simples (código existente)
        else:
            if self.target.type == self.value.type:
                result += f"STOREG {symbol_table.get_stack_pos(self.target.name)}\n"
            else:
                if self.target.type.lower() == "real" and self.value.type.lower() == "integer":
                    result += "ITOF\n"
                    result += f"STOREG {symbol_table.get_stack_pos(self.target.name)}\n"
                else: 
                    raise Exception(f"Cannot assign {self.value.type} to {self.target.type}")
        
        return result
      

class BinaryOp(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right
        self.type = None  # Will be set after validation
        self.value = None  # Will be set after validation

        self.validate_and_infer_type()

    def validate_and_infer_type(self):
        lt = self.left.type
        rt = self.right.type
        op = self.op.lower()

        numeric_ops = ["+", "-", "*", "/", "div", "mod", "=", "<", "<=", ">", ">=", "<>"]
        boolean_ops = ["and", "or"]
        char_ops = ["=", "<", "<=", ">", ">=", "<>"]

        if lt == "string" and rt == "string":
            if op != "+":
                raise Exception(f"Operation '{self.op}' not valid for strings")
            self.type = "string"

        elif lt in ["integer", "real"] and rt in ["integer", "real"]:
            if op not in numeric_ops:
                raise Exception(f"Operation '{self.op}' not valid for numeric types")
            if op in ["+", "-", "*", "/", "div"]:
                self.type = "real" if "real" in [lt, rt] else "integer"
            elif op in ["mod"]:
                self.type = "integer"
            else:
                self.type = "boolean"

        elif lt == "boolean" and rt == "boolean":
            if op not in boolean_ops:
                raise Exception(f"Operation '{self.op}' not valid for booleans")
            self.type = "boolean"

        elif lt == "char" and rt == "char":
            if op not in char_ops:
                raise Exception(f"Operation '{self.op}' not valid for chars")
            self.type = "boolean"

        elif (lt == "char" and rt == "string") or (rt == "char" and lt == "string"):
            if op == "+":
                self.type = "string"
            else:
                raise Exception(f"Operation '{self.op}' not valid for char and string")

        else:
            raise Exception(f"Incompatible types for '{self.op}': {lt}, {rt}")


    def calc_func(self, left, right, op):
        lval, rval = left.value, right.value
        ltype, rtype = left.type, right.type
        op = op.lower()

        # Define operator functions
        arithmetic_ops = {
            "+": operator.add,
            "-": operator.sub,
            "*": operator.mul,
        }
        division_ops = ["/", "div", "mod"]
        comparison_ops = {
            "=": operator.eq,
            "<>": operator.ne,
            ">": operator.gt,
            "<": operator.lt,
            ">=": operator.ge,
            "<=": operator.le,
        }
        logical_ops = {
            "and": lambda a,b: bool(a) and bool(b),
            "or": lambda a,b: bool(a) or bool(b),
        }

        # Helper to generate PUSH instructions
        def to_push(val, typ):
            if typ in ["integer", "boolean"]:
                return f"PUSHI {int(val)}\n"
            elif typ == "real":
                return f"PUSHF {val}\n"
            elif typ in ["string", "char"]:
                return f'PUSHS "{val}"\n'
            else:
                raise Exception(f"Unsupported type for push: {typ}")

        # Check division by zero for division-like ops
        if op in division_ops:
            if (rval == 0) or (rtype in ["integer", "real"] and rval == 0):
                raise Exception("Division by zero")

            if op == "/":
                result = lval / rval
                result_type = "real" if "real" in (ltype, rtype) else "integer"
            elif op == "div":
                result = lval // rval
                result_type = "integer"
            elif op == "mod":
                result = lval % rval
                result_type = "integer"

            self.value = result
            return to_push(result, result_type)

        # Arithmetic ops (+, -, *)
        if op in arithmetic_ops:
            # String concatenation special case
            if op == "+" and (ltype in ["string", "char"] or rtype in ["string", "char"]):
                result = str(lval) + str(rval)
                self.value = result
                return to_push(result, "string")

            # Numeric ops
            if ltype in ["integer", "real"] and rtype in ["integer", "real"]:
                result = arithmetic_ops[op](lval, rval)
                result_type = "real" if "real" in (ltype, rtype) else "integer"
                self.value = result
                return to_push(result, result_type)

            raise Exception(f"Operation '{op}' not valid for types {ltype}, {rtype}")

        # Comparison ops (=, <>, >, <, >=, <=)
        if op in comparison_ops:
            # Allow comparisons between numeric, char, string
            if (ltype in ["integer", "real", "char", "string"] and rtype in ["integer", "real", "char", "string"]) or \
            (ltype == rtype):
                result = comparison_ops[op](lval, rval)
                self.value = result
                return to_push(result, "boolean")
            raise Exception(f"Comparison '{op}' not valid for types {ltype}, {rtype}")

        # Logical ops (and, or)
        if op in logical_ops:
            if ltype == "boolean" and rtype == "boolean":
                result = logical_ops[op](lval, rval)
                self.value = result
                return to_push(result, "boolean")
            raise Exception(f"Logical operation '{op}' requires boolean types")

        raise Exception(f"Unsupported operation '{op}' for types {ltype}, {rtype}")


    def generate(self):
        lt = self.left.type
        rt = self.right.type
        op = self.op.lower()
        
        left_code = self.left.generate()
        right_code = self.right.generate()

        # if (isinstance(self.left, Literal) or (isinstance(self.left, BinaryOp) and self.left.value!=None)) and (isinstance(self.right, Literal) or (isinstance(self.left, BinaryOp) and self.left.value!=None)):
        if (self.left.value!=None) and (self.right.value!=None):
            return self.calc_func(self.left, self.right, op)
        else:
            is_float = lt == "real" or rt == "real"

            op_map = {
                # Numeric operations
                "+": lambda: "FADD\n" if is_float else "ADD\n",
                "-": lambda: "FSUB\n" if is_float else "SUB\n",
                "*": lambda: "FMUL\n" if is_float else "MUL\n",
                "/": lambda: "FDIV\n" if is_float else "DIV\n",
                "div": lambda: ("FDIV\nFTOI\n" if is_float else "DIV\nFTOI\n"),
                "mod": lambda: "MOD\n",

                # Relational
                "=": lambda: "EQUAL\n",
                "<": lambda: "FINF\n" if is_float else "INF\n",
                "<=": lambda: "FINFEQ\n" if is_float else "INFEQ\n",
                ">": lambda: "FSUP\n" if is_float else "SUP\n",
                ">=": lambda: "FSUPEQ\n" if is_float else "SUPEQ\n",
                "<>": lambda: "NE\n",

                # Boolean
                "and": lambda: "AND\n",
                "or": lambda: "OR\n",

                # String
                "+_string": lambda: "CONCAT \n",
            }
            
            # Special case for string concatenation
            if (lt == rt == "string" or (lt == "char" and rt == "string") or (rt == "char" and lt == "string")) and op == "+":
                if lt == "char":
                    left_code = self.left.generatestr()
                if rt == "char":
                    right_code = self.right.generatestr()
                return right_code + left_code + op_map["+_string"]()
            
            # Caso de verificação para se um dos números for 0
            if (self.left.value is None or isinstance(self.left.value, (int, float))) and \
                (self.right.value is None or isinstance(self.right.value, (int, float))):
                    if (self.right.value == 0 or self.left.value == 0):
                        if op in ["/", "div", "mod"]:
                            raise Exception("Division by zero")
                        if op == "*":
                            self.value = 0
                            return "PUSHI 0\n" if not is_float else "PUSHF 0.0\n"
                        if op == "+":
                            return left_code if self.right.value == 0 else right_code

                    if (self.right.value == 1 or self.left.value == 1):
                        if op == "*":
                            return left_code if self.right.value == 1 else right_code

            instr = op_map.get(op)
            if instr:
                return left_code + right_code + instr()
            else:
                raise Exception(f"Unsupported operation in code generation: {self.op}")
    

class If(Node):
    def __init__(self, condition, then_block, else_block):
        self.condition = condition      #expressão
        self.then_block = then_block    #lista de comandos
        self.else_block = else_block    #lista de comandos 

    def generate(self):
        label_else = f"ELSE{id(self)}"
        label_end = f"END{id(self)}"
        condition_code = self.condition.generate()
        if self.condition.type != "boolean":
            raise Exception("The if condition isn't a boolean operation")
        code = condition_code + f"JZ {label_else}\n"
        for command in self.then_block:
            code += command.generate()
        code += f"JUMP {label_end}\n"
        code += f"{label_else}:\n"
        if self.else_block is not None:
            for command in self.else_block:
                code += command.generate()            
        code += f"{label_end}:\n"
        return code

class While(Node):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body
        if self.condition.type != "boolean":
            raise Exception("The while condition isn't a boolean operation")

    def generate(self):
        label_start = f"WHILESTART{id(self)}"
        label_end = f"WHILEEND{id(self)}"
        cond_code = self.condition.generate()
        
        body_code = ""
        for bc in self.body:
            body_code += bc.generate()
        code = f"{label_start}:\n"
        code += cond_code + f"JZ {label_end}\n"
        code += body_code + f"JUMP {label_start}\n"
        code += f"{label_end}:\n"
        return code

class Identifier(Node):
    def __init__(self, name):
        self.name = name
        self.value = None
        self.type = symbol_table.symbols.get(self.name)[0]

    def generate(self):
        symbol = symbol_table.symbols.get(self.name)
        return f"PUSHG {symbol[1]}\n"
    
    def generatestr(self):
        symbol = symbol_table.symbols.get(self.name)
        result = f"PUSHG {symbol[1]}\n"
        if self.type.lower() == "integer":
            result = result + """STRI\n"""
        elif self.type.lower() == "real":
            result = result + """STRF\n"""
        return result
    
class Array(Node):
    def __init__(self, identifier, index):
        self.identifier = identifier
        self.index = index
        self.value = None
        symbol = symbol_table.symbols.get(self.identifier.name)
        if isinstance(symbol[0], dict) and symbol[0].get('type') == 'array':
            self.type = symbol[0]['base_type']
        else:
            self.type = "char"

    def generate(self):
        """Gera código para acessar um elemento do array"""
        code = ""
        symbol = symbol_table.symbols.get(self.identifier.name)
        
        # Obter o tipo do elemento do array
        if isinstance(symbol[0], dict) and symbol[0].get('type') == 'array':
            # Carregar o ponteiro do array (já está na heap)
            pos = symbol[1]
            code += f"PUSHG {pos}\n"  # Carrega o ponteiro
            
            # Calcular o índice
            code += self.index.generate()
            
            # Ajustar o índice se o array começa em um valor diferente de 0
            if isinstance(symbol[0], dict) and symbol[0].get('range'):
                min_index = symbol[0]['range'][0]
                if min_index > 0:
                    code += f"PUSHI {min_index}\nSUB\n"
            
            # Acessar o elemento
            code += "LOADN\n"  # Carrega o valor na posição índice
            
            return code
        else:
            if symbol[0] == "string":
                pos = symbol[1]
                code += f"PUSHG {pos}\n"
                code += self.index.generate()
                code+= f"PUSHI 1\nSUB\n"
                code += "CHARAT\n"
                return code
                
    def generatestr(self):
        """Gera código para converter o elemento do array para string"""
        code = self.generate()
        if self.type.lower() == "integer":
            code += "STRI\n"  # Converte inteiro para string
        elif self.type.lower() == "real":
            code += "STRF\n"  # Converte real para string
        return code
        
class For(Node):
    def __init__(self, identifier, start, to_or_downto, end, body):
        self.identifier = identifier
        self.start = start
        self.to_or_downto = to_or_downto
        self.end = end
        self.body = body

    def generate(self):
        label_start = f"FORSTART{id(self)}"
        label_end = f"FOREND{id(self)}"
        pos = symbol_table.get_stack_pos(self.identifier.name)
        code = ""

        # Inicializar o contador
        code += self.start.generate()
        code += f"STOREG {pos}\n"

        # Início do loop
        code += f"{label_start}:\n"
        
        # Verificar condição de paragem
        code += f"PUSHG {pos}\n"    # Valor atual do contador
        code += self.end.generate()  # Valor final
        
        # Comparação baseada na direção (to ou downto)
        if self.to_or_downto.lower() == "to":
            code += "SUP\nNOT\n"   # Inverte SUP para continuar enquanto i <= fim
        else:
            code += "INF\nNOT\n"   # Inverte INF para continuar enquanto i >= fim
            
        code += f"JZ {label_end}\n"  # Sai do loop se a condição for falsa

        # Corpo do laço
        for command in self.body:
            code += command.generate()

        # Incrementar ou decrementar o contador
        code += f"PUSHG {pos}\n"
        if self.to_or_downto.lower() == "to":
            code += "PUSHI 1\nADD\n"
        else:
            code += "PUSHI 1\nSUB\n"
        code += f"STOREG {pos}\n"
        
        # Voltar ao início do loop
        code += f"JUMP {label_start}\n"
        code += f"{label_end}:\n"
        
        return code
       

class Literal(Node):
    def __init__(self, lit_type, value):
        self.type = lit_type
        self.value = value
    def generate(self):
        if self.type == "string":
            escaped = self.value.replace('"', '\\"').replace("\n", "\\n")
            return f'PUSHS "{escaped}"\n'
        elif self.type == "integer":
            return f"""PUSHI {self.value}\n"""
        elif self.type == "real":
            return f"""PUSHF {self.value}\n"""
        elif self.type == "boolean":
            if self.value:
                return f"""PUSHI 1\n"""
            else:
                return f"""PUSHI 0\n"""
        elif self.type == "char":
            return f"""PUSHI {ord(self.value)}\n"""
        
    def generatestr(self):
        if self.type == "string":
            return f'PUSHS "{self.value}"\n'
        elif self.type == "integer":
            return f"""PUSHI {self.value}\n STRI\n"""
        elif self.type == "real":
            return f"""PUSHF {self.value}\n STRF\n"""
        elif self.type == "boolean":
            if self.value:
                return f"""PUSHI 1\n"""
            else:
                return f"""PUSHI 0\n"""
        elif self.type == "char":
            return f"""PUSHS "{self.value}"\n"""
        else:
            raise Exception(f"Unknown literal type: {self.type}")
