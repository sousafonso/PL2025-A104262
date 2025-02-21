import re
import os

# padrão regex para extrair os campos do CSV
regex_pattern = re.compile(r'([^;]+);("(?:[^"]*(?:"[^"]*)*)"|[^;]+);([^;]+);([^;]+);([^;]+);([^;]*)\n?')

# Conjunto para armazenar os compositores únicos
compositores_set = set()

# Dicionários para armazenar a contagem e os títulos por período
contagem_periodo = {}
titulos_por_periodo = {}

# Abre o arquivo CSV e ignora o cabeçalho
with open("./TPC2/obras.csv", 'r', encoding='utf-8') as file_in:
    file_in.readline()  # Ignora o cabeçalho
    acumulador = ""
    
    for line in file_in:
        acumulador += line
        resultado = re.match(regex_pattern, acumulador)
        if resultado:
            titulo = resultado.group(1)
            periodo = resultado.group(4)
            compositor = resultado.group(5)
            
            # Adiciona o compositor ao conjunto
            compositores_set.add(compositor)
            
            # Atualiza a contagem de obras por período
            if periodo in contagem_periodo:
                contagem_periodo[periodo] += 1
            else:
                contagem_periodo[periodo] = 1
            
            # Agrupa os títulos das obras por período
            if periodo not in titulos_por_periodo:
                titulos_por_periodo[periodo] = []
            titulos_por_periodo[periodo].append(titulo)
            
            # Reseta o acumulador para a próxima linha(s)
            acumulador = ""

# Ordena os compositores e os títulos
compositores_ordenados = sorted(compositores_set)
for per in titulos_por_periodo:
    titulos_por_periodo[per].sort()

# Se o arquivo de saída já existir, remove-o
if os.path.exists("outputs.txt"):
    os.remove("outputs.txt")

# Grava os resultados no arquivo e os exibe no console
with open("outputs.txt", 'a', encoding='utf-8') as out_file:
    # 1. Lista de compositores ordenada
    out_file.write("1. Lista ordenada alfabeticamente dos compositores:\n")
    out_file.write(str(compositores_ordenados) + "\n\n")
    
    # 2. Distribuição das obras por período
    out_file.write("2. Distribuição das obras por período:\n")
    for per in sorted(contagem_periodo.keys()):
        out_file.write(f"{per}: {contagem_periodo[per]} obras\n")
    out_file.write("\n")
    
    # 3. Dicionário de títulos por período com listas ordenadas
    out_file.write("3. Dicionário por período com lista alfabética dos títulos:\n")
    for per in sorted(titulos_por_periodo.keys()):
        out_file.write(f"{per}: {titulos_por_periodo[per]}\n")

print("1. Lista ordenada alfabeticamente dos compositores:")
print(compositores_ordenados)

print("\n2. Distribuição das obras por período:")
for per in sorted(contagem_periodo.keys()):
    print(f"{per}: {contagem_periodo[per]} obras")

print("\n3. Dicionário por período com lista alfabética dos títulos:")
for per in sorted(titulos_por_periodo.keys()):
    print(f"{per}: {titulos_por_periodo[per]}")