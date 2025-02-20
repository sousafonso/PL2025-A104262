# Caminho do ficheiro CSV
file_path = "./TPC2/obras.csv"

# Ler todas as linhas do ficheiro
with open(file_path, "r", encoding="utf-8") as file:
    lines = file.readlines()

# O cabeçalho está contido na primeira linha (separado por ponto-e-vírgula)
header = lines[0].strip().split(";")
data = [line.strip().split(";") for line in lines[1:] if line.strip() and len(line.strip().split(";")) >= len(header)]

# Obter os índices das colunas relevantes
idx_nome = header.index("nome")
idx_compositor = header.index("compositor")
idx_periodo = header.index("periodo")

# 1. Lista ordenada alfabeticamente dos compositores musicais
compositores = sorted({row[idx_compositor] for row in data})

# 2. Distribuição das obras por período (quantas obras em cada período)
distribuicao_obras = {}
for row in data:
    periodo = row[idx_periodo]
    distribuicao_obras[periodo] = distribuicao_obras.get(periodo, 0) + 1

# 3. Dicionário com, para cada período, uma lista alfabética dos títulos das obras
obras_por_periodo = {}
for row in data:
    periodo = row[idx_periodo]
    obra = row[idx_nome]
    if periodo not in obras_por_periodo:
        obras_por_periodo[periodo] = []
    obras_por_periodo[periodo].append(obra)

# Ordenar alfabeticamente os títulos em cada período
for periodo in obras_por_periodo:
    obras_por_periodo[periodo] = sorted(obras_por_periodo[periodo])

# Exibir os resultados
print("Lista ordenada dos compositores:")
for compositor in compositores:
    print(" -", compositor)

print("\nDistribuição das obras por período:")
for periodo, quantidade in distribuicao_obras.items():
    print(f" {periodo}: {quantidade} obra(s)")

print("\nObras por período (títulos ordenados alfabeticamente):")
for periodo, obras in obras_por_periodo.items():
    print(f"\nPeríodo: {periodo}")
    for obra in obras:
        print("   -", obra)
