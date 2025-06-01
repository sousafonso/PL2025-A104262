class SymbolTable():
    def __init__(self):
        self.symbols = {}   # var_name : (type, stack_position)
        self.stack_pos = 0  #Current stack position
        #self.parent = None

    def add(self, var_list, var_type):
        for var in var_list:
            if var in self.symbols:
                raise Exception(f"Variable '{var}' already declared.")
            
            # Se for um array, calculamos o tamanho necessário
            if isinstance(var_type, dict) and var_type.get('type') == 'array':
                array_range = var_type.get('range', (0, 0))
                array_size = array_range[1] - array_range[0] + 1
                
                # Registramos o tipo, posição na pilha e o tamanho do array
                self.symbols[var] = (var_type, self.stack_pos, array_size)
                self.stack_pos += 1  # Apenas um slot na pilha para referência ao array
            else:
                # Variável simples
                self.symbols[var] = (var_type.lower(), -1)
                #self.stack_pos += 1

    def get_stack_pos(self, var_name):
        symbol = self.symbols.get(var_name)

        if symbol is None:
            raise Exception(f"Variable '{var_name}' not declared.")
        if symbol[1] == -1:
            self.symbols[var_name] = (symbol[0], self.stack_pos)
            self.stack_pos += 1
        return self.symbols[var_name][1]
    
    def check_declarations(self):
        for key, value in self.symbols.items():
            if value[1] == -1:
                print(f"// Variable '{key}' declared but never used.")
        
    
symbol_table = SymbolTable()

