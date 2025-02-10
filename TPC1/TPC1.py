def somaDigitos(texto):
    soma = 0
    i = 0
    texto2 = texto.lower() # para nao termos de controlar a combinação de maiúsculas e minúsculas, 
    acumulando = True  

    while i < len(texto2):
        if texto2[i:i+3] == "off":
            acumulando = False
            i += 3
        elif texto2[i:i+2] == "on":
            acumulando = True
            i += 2
        elif texto2[i] == "=":
            print(soma)
            i += 1
        elif acumulando and texto2[i] in "0123456789":
            minha_string = "" # string vazia que vai acumulando os digitos formando números da forma string
            while i < len(texto2) and texto2[i] in "0123456789":
                minha_string += texto2[i]
                i += 1
            if minha_string:
                soma += int(minha_string) # somando e convertendo para inteiro a string construída com os digitos
        else:
            i += 1

    return soma