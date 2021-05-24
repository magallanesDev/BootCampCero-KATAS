campos = ('Nombre', 'Apellido', 'Matemáticas', 'Lengua', 'Naturales', 'Sociales')
notas = [('Pedro', 'Jiménez', 10, 9, 8, 9), ('Juana', 'Rodríguez', 9, 4, 9, 8), ('Andrés', 'Stevensson', 6, 7, 9, 5)]

boletinesObjetivo = [{'Nombre': 'Pedro', 'Apellido': 'Jiménez', 'Matemáticas': 10, 'Lengua': 9, 'Naturales': 8, 'Sociales': 9},
            {'Nombre': 'Juana', 'Apellido': 'Rodríguez', 'Matemáticas': 9, 'Lengua': 4, 'Naturales': 9, 'Sociales': 8},
            {'Nombre': 'Andrés', 'Apellido': 'Stevensson', 'Matemáticas': 6, 'Lengua': 7, 'Naturales': 9, 'Sociales': 5}]

boletines = []
for nota in notas:
    contador = 0
    diccionario = {}
    for elemento in nota:
        diccionario[campos[contador]] = elemento
        contador += 1
    
    media = (nota[2] + nota[3] + nota[4] + nota[5]) / 4
    diccionario['media'] = media
    
    numAsteriscos = int(media // 0.5)
    asteriscos = []
    for letra in range(0, numAsteriscos):
        asteriscos.append('*')
    resto = media % 0.5
    if resto != 0:
        asteriscos.append('*')
    strAsteriscos = ''.join(asteriscos)
    print(len(strAsteriscos))
    diccionario['gráfico'] = strAsteriscos
    boletines.append(diccionario)
        
print(boletines)
