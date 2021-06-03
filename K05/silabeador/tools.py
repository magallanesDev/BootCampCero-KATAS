consonantes = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l',  'm', 'n', 'ñ', 'p', 'q', 'r',  's', 't', 'v', 'w', 'x', 'z']
consonantes_dobles = ['bs', 'll', 'rr', 'bl', 'cl', 'gl', 'fl', 'kl', 'pl', 'br', 'cr', 'dr', 'fr', 'gr', 'kr', 'pr', 'tr', 'ps', 'ch']
vocales_abiertas = ['a', 'e', 'o', 'á', 'é', 'í', 'ó', 'ú']
vocales_cerradas = ['i', 'u', 'ü']
semivocales = ['y']
_INTERSILABA = 'pi'
def pipalabra(word):
    silabas = silabea(word)
    newword = _INTERSILABA+ _INTERSILABA.join(silabas)
    return newword
def pilengua(word):
    if ' ' in word:
        newphrase = []
        palabras = word.split()
        for palabra in palabras:
            newword = silabea(palabra)
            if newword and newword[0][0].lower() == 'r':
                newword[0] = newword[0][0] + newword[0]
            newword = _INTERSILABA + _INTERSILABA.join(newword) 
            newphrase.append(newword)
        return ' '.join(newphrase).lower()
    else:
        return pipalabra(word)
def busca(word, cadena):
    try:
        return word.index(cadena)
    except ValueError:
        return -1
def inversa(word):
    original = ''
    contJumps = 1
    p1 = word[2*contJumps+len(original):]
    while len(p1) > 2:
        froc = silabea(p1)
        original += froc[0]
        contJumps += 1
        p1 = word[2*contJumps+len(original):]
    #procesa doble R
    original = original.lower()
    if original[0:2] == 'rr':
        original = original[1:]
    pos = busca(original, (' rr'))
    while pos != -1:
        original = original[:pos+1]+original[pos+2:]
        pos = busca(original, (' rr'))
    return original
def esDiptongo(position, word):
    if len(word) < position + 2:
        return False
    return (word[position] in vocales_cerradas and word[position+1] in vocales_cerradas) or \
           (word[position] in vocales_cerradas and word[position+1] in semivocales) or \
           (word[position] in vocales_abiertas and (word[position+1] in vocales_cerradas or word[position+1] in semivocales)) or \
           (word[position] in vocales_cerradas and word[position+1] in vocales_abiertas)
def esTriptongo(position, word):
    if len(word) < position + 3:
        return False
    return (word[position] in vocales_cerradas and word[position+1] in vocales_abiertas and (word[position+2] in vocales_cerradas or word[position+2] in semivocales))
def gruposVocales(word):
    grupos = []
    jump = 0
    for position, caracter in enumerate(word):
        if jump:
            jump-=1
            continue
        if caracter in vocales_abiertas or caracter in vocales_cerradas:
            if esTriptongo(position, word):
                grupo = (position, word[position: position + 3])
                jump = 2
            elif esDiptongo(position, word):
                grupo = (position, word[position: position + 2])
                jump = 1
            else:
                grupo = (position, word[position])
                jump = 0
            grupos.append(grupo)
        elif caracter in semivocales:
            grupo = (position, word[position])
            jump = 0
            grupos.append(grupo)
    return grupos
def laConsonante(word, position, delante=True):
    if position < 0 or position >= len(word):
        return None
    if position == 0 and delante or position == len(word)-1 and not delante :
        return None
    position += -1 if delante else 1
    if position > 0 and delante:
        consonante = word[position-1:position+1] if word[position-1:position+1] in consonantes_dobles else None
        if consonante:
            return consonante
    consonante = word[position] if word[position] in consonantes or (word[position] in semivocales if delante else False) else None
    return consonante
def consonantesDelante(word, groups):
    if len(groups) == 0:
        return None
    for ix, group in enumerate(groups):
        consonanteDelante = laConsonante(word, group[0]) 
        if consonanteDelante:
            position = group[0]-len(consonanteDelante)
            newGroup = (position, consonanteDelante + group[1])
            groups[ix] = newGroup 
    return groups
def restoHuecos(word, groups):
    if len(groups) == 0:
        return None
    for ix, group in enumerate(groups):
        if ix > 0 and group[0] > 0:
            groupPrev = groups[ix-1]
            if groupPrev[0] + len(groupPrev[1]) < group[0]:
                groups[ix-1] = (groupPrev[0], word[groupPrev[0]:group[0]])
    if groups[ix][0]+len(groups[ix][1]) < len(word):
        groups[ix] = (groups[ix][0], word[groups[ix][0]-len(word):])
    return groups
def excepciones(word, groups):
    '''
     palabras que empiezan por in y cuya segunda silaba acaba por consonante
        i-nac-ción => in-ac-ción
        i-nad-mi-si-ble => in-ad-mi-si-ble
    '''
    if len(groups) >=2 and groups[0] == (0, 'i') and groups[1][1][0] == 'n' and groups[1][1][-1] in consonantes:
        groups[0] = (0, word[0:2])
        groups[1] = (2, groups[1][1][1:])
    '''
     palabras con diptono uy en que y realmente es consonante
        fluyó: fluy-yó => flu-yó
    '''
    if 'y' in word:
        for ix, group in enumerate(groups):
            if ix < len(groups)-1:
                if group[1][-1] == 'y' and groups[ix+1][1][0] == 'y':
                    groups[ix] = (group[0], group[1][:-1])
    return groups
def silabea(w):
    word = w.lower()
    g = gruposVocales(word)
    g = consonantesDelante(word, g)
    g = restoHuecos(word, g)
    g = excepciones(word, g)
    silabas = [item[1] for item in g]
    caseSilabas = []
    ix = 0
    for silaba in silabas:
        caseSilabas.append(w[ix: ix+len(silaba)])
        ix+=len(silaba)
    return caseSilabas