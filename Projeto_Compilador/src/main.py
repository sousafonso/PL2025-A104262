import sys
from pascal_yacc import parser
import pascal_yacc
from symbol_table import symbol_table

def main():
    if len(sys.argv) < 3:
        print("Use: main.py <arquivo_entrada> <arquivo_saida>")
        sys.exit(1)
        
    input_file = sys.argv[1]
    output_file = sys.argv[2]
    
    with open(input_file, "r", encoding="utf8") as f:
        programa = f.read()
        
    r = parser.parse(programa)
    if r is None or pascal_yacc.parse_error_occurred:
        print("Could not compile program.")
        sys.exit(1)
    codigo_maquina = r.generate()
    symbol_table.check_declarations()
    print(codigo_maquina)
    with open(output_file, "w", encoding="utf8") as f:
        f.write(codigo_maquina)
        
    print("// Code compiled in:", output_file)
    
if __name__ == "__main__":
    main()