import json
from datetime import datetime

# Constantes
STOCK_FILE = "stock.json"
MOEDAS_VALIDAS = {"1e": 100, "50c": 50, "20c": 20, "10c": 10, "5c": 5, "2c": 2, "1c": 1}

# Função para carregar o stock do ficheiro JSON
def carregar_stock():
    try:
        with open(STOCK_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Erro: Ficheiro '{STOCK_FILE}' não encontrado.")
        return []

# Função para salvar o stock no ficheiro JSON
def salvar_stock(stock):
    with open(STOCK_FILE, "w", encoding="utf-8") as f:
        json.dump(stock, f, indent=4, ensure_ascii=False)

# Função para listar os produtos
def listar_produtos(stock):
    print("\ncod | nome | quantidade | preço")
    print("---------------------------------")
    for produto in stock:
        print(f"{produto['cod']} | {produto['nome']} | {produto['quant']} | {produto['preco']}€")
    print()

# Função para processar moedas inseridas
def processar_moedas(moedas):
    saldo = 0
    for moeda in moedas:
        if moeda in MOEDAS_VALIDAS:
            saldo += MOEDAS_VALIDAS[moeda]
        else:
            print(f"maq: Moeda inválida: {moeda}")
    return saldo

# Função para formatar o saldo em euros e cêntimos
def formatar_saldo(saldo):
    euros = saldo // 100
    centimos = saldo % 100
    return f"{euros}e{centimos}c" if euros > 0 else f"{centimos}c"

# Função principal
def maquina_vending():
    # Carregar stock
    stock = carregar_stock()
    if not stock:
        print("maq: Erro ao carregar o stock. A encerrar...")
        return

    # Inicializar saldo
    saldo = 0

    # Mensagem de boas-vindas
    print(f"maq: {datetime.now().strftime('%Y-%m-%d')}, Stock carregado, Estado atualizado.")
    print("maq: Bom dia. Estou disponível para atender o seu pedido.")

    # Loop de interação
    while True:
        comando = input(">> ").strip().upper()

        if comando == "LISTAR":
            listar_produtos(stock)

        elif comando.startswith("MOEDA"):
            moedas = comando[6:].strip(" .").split(", ")
            saldo += processar_moedas(moedas)
            print(f"maq: Saldo = {formatar_saldo(saldo)}")

        elif comando.startswith("SELECIONAR"):
            codigo = comando.split()[1]
            produto = next((p for p in stock if p["cod"] == codigo), None)

            if not produto:
                print("maq: Produto inexistente.")
            elif produto["quant"] == 0:
                print("maq: Produto esgotado.")
            elif saldo < produto["preco"] * 100:
                print(f"maq: Saldo insuficiente para satisfazer o seu pedido")
                print(f"maq: Saldo = {formatar_saldo(saldo)}; Pedido = {produto['preco']}€")
            else:
                saldo -= produto["preco"] * 100
                produto["quant"] -= 1
                print(f'maq: Pode retirar o produto dispensado "{produto["nome"]}"')
                print(f"maq: Saldo = {formatar_saldo(saldo)}")

        elif comando == "SAIR":
            if saldo > 0:
                troco = {}
                for moeda, valor in sorted(MOEDAS_VALIDAS.items(), key=lambda x: -x[1]):
                    if saldo >= valor:
                        troco[moeda] = saldo // valor
                        saldo %= valor
                print("maq: Pode retirar o troco:", ", ".join([f"{v}x {k}" for k, v in troco.items()]))
            print("maq: Até à próxima")
            salvar_stock(stock)
            break

        elif comando.startswith("ADICIONAR"):
            try:
                codigo = input("Código do produto: ").strip()
                nome = input("Nome do produto: ").strip()
                quant = int(input("Quantidade: ").strip())
                preco = float(input("Preço (em euros): ").strip())
                produto = {"cod": codigo, "nome": nome, "quant": quant, "preco": preco}
                stock.append(produto)
                print("maq: Produto adicionado com sucesso.")
            except ValueError:
                print("maq: Entrada inválida.")

        else:
            print("maq: Comando inválido.")

# Executar a máquina de vending
if __name__ == "__main__":
    maquina_vending()