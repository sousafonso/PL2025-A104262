class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0
        self.current_token = self.tokens[self.pos] if self.tokens else None

    def advance(self):
        self.pos += 1
        self.current_token = self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def parse(self):
        return self.E()

    def E(self):
        """E → T E'"""
        left = self.T()
        return self.E_prime(left)

    def E_prime(self, left):
        """E' → + T E' | - T E' | ε"""
        if self.current_token in ('+', '-'):
            op = self.current_token
            self.advance()
            right = self.T()
            if op == '+':
                result = left + right
            else:
                result = left - right
            return self.E_prime(result)
        return left

    def T(self):
        """T → F T'"""
        left = self.F()
        return self.T_prime(left)

    def T_prime(self, left):
        """T' → * F T' | / F T' | ε"""
        if self.current_token in ('*', '/'):
            op = self.current_token
            self.advance()
            right = self.F()
            if op == '*':
                result = left * right
            else:
                result = left / right
            return self.T_prime(result)
        return left

    def F(self):
        """F → ( E ) | num"""
        if self.current_token == '(':
            self.advance()
            result = self.E()
            if self.current_token != ')':
                raise SyntaxError("Esperado ')'")
            self.advance()
            return result
        elif self.current_token.isdigit():
            num = int(self.current_token)
            self.advance()
            return num
        else:
            raise SyntaxError(f"Token inesperado: {self.current_token}")

# Exemplo de uso:
def tokenize(expression):
    import re
    tokens = re.findall(r'\d+|[()+*/-]', expression)
    return tokens

expr = "67-(2+3*4)"
tokens = tokenize(expr)
parser = Parser(tokens)
result = parser.parse()
print(f"Resultado de '{expr}': {result}")