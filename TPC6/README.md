# Explicação do Programa

Este projeto implementa um analisador sintático (parser) para expressões aritméticas simples. A seguir, são detalhados os componentes, regras, limitações e funcionamento geral do programa.

## Componentes Principais

- **Tokenização**  
  A função `tokenize` utiliza uma expressão regular para separar a expressão de entrada em tokens.  
  - Reconhece números inteiros (sequências de dígitos) e os seguintes operadores/símbolos: `+`, `-`, `*`, `/`, `(`, `)`.  
  - Exemplo de expressão: `"67-(2+3*4)"`.

- **Parser (Analisador Sintático)**  
  A classe `Parser` implementa um parser recursivo descendente com as seguintes regras gramaticais:
  - **E** → T E'  
  - **E'** → `+` T E' 
            | `-` T E'
            | ε (vazio)
  - **T** → F T'  
  - **T'** → `*` F T' 
            | `/` F T' 
            | ε (vazio)
  - **F** → `( E )` 
            | num

  Cada método na classe (como `E`, `E_prime`, `T`, `T_prime` e `F`) representa uma regra da gramática.

## Funcionamento

1. **Tokenização**:  
   A função `tokenize` recebe uma string com a expressão e retorna uma lista de tokens extraídos usando regex.

2. **Parsing**:  
   Após a tokenização, uma instância de `Parser` é criada com a lista de tokens.  
   O método `parse` inicia o processo de parsing a partir da regra `E`.  
   Durante o parsing:
   - A regra `E` lida com expressões que envolvem adição e subtração.
   - A regra `T` lida com multiplicação e divisão.
   - A regra `F` lida com parênteses e números individuais.
   - A função `advance` é utilizada para mover o ponteiro de tokens para o próximo token.

3. **Cálculo da Expressão**:  
   Conforme os métodos vão processando a expressão, as operações aritméticas são executadas e o resultado final é calculado e exibido.

## Regras e Limitações

- **Regras Estabelecidas**:
  - A gramática define corretamente as precedências dos operadores: operações em parênteses e multiplicação/divisão são avaliadas antes de adição/subtração.
  - O parser utiliza recursão para processar expressões de comprimento arbitrário, conforme delimitado pela grammatical definida.

- **Limitações**:
  - Apenas números inteiros são suportados, pois a tokenização utiliza `\d+` e a verificação com `.isdigit()`. 
  - Expressões com números decimais ou negativos não são tratados.
  - Não há suporte para tratamento de espaços em branco explicitamente; a regex depende da formatação da string de entrada.
  - Em caso de erro, como o número de parênteses esperados ou tokens inesperados, é lançada uma exceção `SyntaxError`.

## Exemplo de Uso

```python
expr = "67-(2+3*4)"
tokens = tokenize(expr)
parser = Parser(tokens)
result = parser.parse()
print(f"Resultado de '{expr}': {result}")
```
---
## Autoria
- **Nome**: Afonso Sousa
- **Número**: A104262