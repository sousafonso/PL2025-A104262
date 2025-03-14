# Documentação do TPC5 – Máquina de Vending

## Objetivo

O objetivo deste TPC é construir um programa que simule o funcionamento de uma máquina de vending. A máquina deverá:

- Carregar e guardar o stock de produtos num ficheiro JSON, permitindo persistir o estado da aplicação entre execuções.
- Permitir ao utilizador listar os produtos disponíveis no stock.
- Processar a inserção de moedas para aumentar o saldo.
- Permitir ao utilizador seleccionar um produto (se existir e estiver disponível em stock) e, se o saldo for suficiente, efetuar a compra.
- Dispensar um troco, quando aplicável, e encerrar a sessão.
- **Funcionalidade extra – ADICIONAR:**  
  Permitir ao utilizador acrescentar novos produtos ou atualizar produtos existentes ao stock, especificando o código, nome, quantidade e preço.

## Funcionamento

1. **Persistência do Stock:**  
   O stock de produtos é guardado num ficheiro `stock.json`.  
   Cada produto é representado por um dicionário com os campos:
   - `cod`: código do produto (ex.: "A23")
   - `nome`: nome do produto (ex.: "água 0.5L")
   - `quant`: quantidade disponível
   - `preco`: preço unitário (em euros)

   Ao iniciar o programa, o ficheiro é carregado, e no final da sessão o stock atualizado é salvo, permitindo manter o estado entre execuções.

2. **Interação com o Utilizador:**  
   Após apresentar uma mensagem de boas-vindas com a data atual indicando que o stock foi carregado e o estado atualizado, a máquina de vending aceita os seguintes comandos através da consola:
   
   - **LISTAR:**  
     Exibe os produtos disponíveis com o seu código, nome, quantidade e preço.
   
   - **MOEDA [valores]:**  
     Permite a inserção de moedas para aumentar o saldo.  
     As moedas válidas são definidas na constante `MOEDAS_VALIDAS` (ex.: "1e", "50c", "20c", etc.).  
     Exemplo de utilização:  
     `MOEDA 1e, 20c, 5c, 5c .`
   
   - **SELECIONAR [código]:**  
     Permite seleccionar um produto através do seu código.  
     Se o produto existir, estiver em stock e o saldo for suficiente para cobrir o seu preço, o produto é dispensado, o stock é atualizado e o saldo deduzido.  
     Caso o saldo seja insuficiente ou o produto não esteja disponível, uma mensagem informativa é apresentada.
   
   - **ADICIONAR:**  
     Permite ao utilizador adicionar um novo produto ou atualizar um produto existente no stock.  
     Ao utilizar este comando, o programa solicita a introdução dos dados do produto (código, nome, quantidade e preço).
   
   - **SAIR:**  
     Termina a sessão. Se existir saldo remanescente, a máquina calcula e exibe o troco a ser devolvido ao utilizador, e o stock atualizado é então guardado.

3. **Processamento das Moedas e Cálculo do Troco:**  
   - As moedas inseridas são convertidas para cêntimos e acumuladas no saldo.
   - No comando SAIR, se houver saldo, o programa calcula o troco com base nas moedas disponíveis e apresenta a quantidade de cada moeda a ser devolvida.

## Considerações

- Caso o ficheiro `stock.json` não seja encontrado, o programa apresenta uma mensagem de erro e encerra a execução.
- São contemplados diversos cenários, como: produto inexistente, produto esgotado, saldo insuficiente, moeda inválida, etc.
- A implementação permite a persistência do stock entre execuções e simula a interação com uma máquina de vending real através de comandos escritos na consola.

---

## Autoria

- **Nome:** Afonso Sousa
- **ID:** A104262