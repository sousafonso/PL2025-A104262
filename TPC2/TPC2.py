import re
import os

# padrão regex para extrair os campos do CSV
regex_pattern = re.compile(
    r'([^;]+);("(?:[^"]*(?:"[^"]*)*)"|[^;]+);([^;]+);([^;]+);([^;]+);([^;]*)\n?'
)

# Conjunto para armazenar os compositores únicos
compositores_set = set()

# Dicionários para armazenar a contagem e os títulos por período
contagem_periodo = {}
titulos_por_periodo = {}

# Abre o ficheiro CSV e ignora o cabeçalho
with open("./TPC2/obras.csv", "r", encoding="utf-8") as file_in:
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
            
            # Reseta o acumulador para a próxima(s) linha(s)
            acumulador = ""

# Ordena os compositores e os títulos
compositores_ordenados = sorted(compositores_set)
for per in titulos_por_periodo:
    titulos_por_periodo[per].sort()

# Exibe os resultados no terminal

print("1. Lista ordenada alfabeticamente dos compositores:")
print(compositores_ordenados)

print("\n2. Distribuição das obras por período:")
for per in sorted(contagem_periodo.keys()):
    print(f"{per}: {contagem_periodo[per]} obras")

print("\n3. Dicionário por período com lista alfabética dos títulos:")
for per in sorted(titulos_por_periodo.keys()):
    print(f"{per}: {titulos_por_periodo[per]}")