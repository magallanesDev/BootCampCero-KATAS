simbolos = {
    '1': ['1', '¿', '?', '¡', '!'],
    '2': ['2', 'A', 'B', 'C'],
    '3': ['3', 'D', 'E', 'F'],
    '4': ['4', 'G', 'H', 'I'],
    '5': ['5', 'J', 'K', 'L'],
    '6': ['6', 'M', 'N', 'Ñ', 'O'],
    '7': ['7', 'P', 'Q', 'R', 'S'],
    '8': ['8', 'T', 'U', 'V'],
    '9': ['9', 'W', 'X', 'Y', 'Z'],
    '0': [' ', '.', ',', ';', ':']
    }

def caracter_a_tecla(c):
    for tecla in simbolos.keys():
        if c in simbolos[tecla]:
            pos = simbolos[tecla].index(c)
            return (pos+1)*tecla
    
    return '_'




def traduce(cadena):
    cadena = cadena.upper()
    r = ''
    for caracter in cadena:
        r += caracter_a_tecla(caracter) + ''
    return r[:-1]




