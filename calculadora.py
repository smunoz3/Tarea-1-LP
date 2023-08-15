import re

def list_to_str(lista):
    '''
    ***
    * lista : Tipo lista
    ***
    Toma una lista y la convierte en string.
    Retorna un string
    '''
    string = ""
    i = 0
    while lista[i] != lista[-1]:
        string=string + lista[i] + " "
        i += 1
    string=string + lista[i]
    return string

def resolver_prioridad_1(texto):
    '''
    ***
    * texto : Tipo lista
    ***
    Toma una lista la recorre y va resolviendo las opereraciones de producto y division
    Retorna una lista
    '''
    i = 0 
    while texto[i] != texto[-1]:
        if texto[i] == "ANS":
            texto[i]= str(ans)
        if texto[i+1] == "ANS":
            texto[i+1]= str(ans)
        if texto[i] == "*":
            z = int(texto[i-1])*int(texto[i+1])
            texto[i+1]= str(z)
            del texto[i]
            del texto[i-1]
            i -= 2
        elif texto[i] == "//":
            z = int(texto[i-1])//int(texto[i+1])
            texto[i+1]= str(z)
            del texto[i]
            del texto[i-1]
            i -= 2
        i += 1
    return texto

def resolver_prioridad_2(texto):
    '''
    ***
    * texto : Tipo lista
    ***
    Toma una lista la recorre y va resolviendo las opereraciones de suma y resta
    Retorna una lista
    '''
    i = 0
    while texto[i] != texto[-1]:
        if texto[i] == "ANS":
            texto[i]= str(ans)
        if texto[i+1] == "ANS":
            texto[i+1]= str(ans)
        if texto[i] == "+":
            z = int(texto[i-1])+int(texto[i+1])
            texto[i+1]= str(z)
            del texto[i]
            del texto[i-1]
            i -= 2
        elif texto[i] == "-":
            z = int(texto[i-1])-int(texto[i+1])
            texto[i+1]= str(z)
            del texto[i]
            del texto[i-1]
            i -= 2
        i += 1
    return texto

def Cupon_simple(x):
    '''
    ***
    * x : Tipo int
    ***
    Recibe un numero retorna su 20%
    Retorna un int
    '''
    s = int(x) * 0.2
    return int(s)

def Cupon_doble(x,y):
    '''
    ***
    * x : Tipo int
    * y : Tipo int
    ***
    Recibe un numero retorna su y%
    Retorna un int
    '''
    z = float(y) / 100.0
    s = int(x) * z
    return int(s)

def validacion_operacion(texto):
    '''
    ***
    * texto : 
    ***
    describe la funcion
    '''
    retorno = True
    operaciones = r'\+|\-|\*|\//'
    valido_1 = ['0','1','2','3','4','5','6','7','8','9','S',')']
    valido_2 = ['0','1','2','3','4','5','6','7','8','9','A','C','(']
    matches = [match.start() for match in re.finditer(operaciones, texto)]
    for i in matches:
        if texto[i] == "/":
            if not ((texto[i-1] in valido_1) and (texto[i+2] in valido_2)):
                retorno = False
        elif not ((texto[i-1] in valido_1) and (texto[i+1] in valido_2)):
            retorno = False
    return retorno

def revision_errores(text):
    '''
    ***
    * text : 
    ***
    describe la funcion
    '''
    text = re.sub(r'\s+', '', text)
    contador=0
    for i in text:
        if i == "(":
            contador +=1
        elif i == ")":
            contador -=1
        if contador <0:
            return False
    if contador != 0:
        return False
    if len(re.findall("\/0", text)) != 0:
        return False
    if validacion_operacion(text) == False:
        return False
    temp = re.findall(r'[0-9]+\(|\)[0-9]+|(\+|\-|\*|\//|[0-9]+|ANS )\([0-9]+\)', text)
    if (len(re.findall(r'[0-9]+\(|\)[0-9]+|(\+|\-|\*|\//|[0-9]+|ANS)\([0-9]+\)', text)) != 0):
        return False
    if (len(re.findall(r'(CUPON\(CUPON\()|(CUPON\(\))|(CUPON\([0-9]+,\))',text))!=0): #detecta CUPON(CUPON y CUPON(  )
        return False
    if (len(re.findall(r'^(\+|\-|\*|\//)[0-9]+',text))) !=0:#partir con operaciones
        return False
    #temp2 = r'[^\bANS\b]'
    #r = re.findall(r'[^\bANS\b]',text)
    if (len(re.findall(r'[^(\d|\+|\-|\*|\//|ANS|CUPON|CUPON\(\d,\d)]',text))!=0):
        return False
    if (len(re.findall(r'CUPON\(\d(\+|\-|\*|\//)',text)))!=0: #operaciones dentro de parencis
        return False
    if (len(re.findall(r'ANS'))!=0):
        if len(re.findall(r'[^\bANS\b]',text))!=0:
            return False
    return True

def resolver_problema(text):
    '''
    ***
    * text : 
    ***
    describe la funcion
    '''
    cupon_1 = re.compile(r'CUPON\(\s*[0-9]+\s*\)')
    resultados_1 = cupon_1.findall(text)
    cupon_2 = re.compile(r'CUPON\(\s*[0-9]+\s*\,\s*[0-9]+\s*\)')
    resultados_2 = cupon_2.findall(text)
    if len(resultados_1) >0:
        for resultado in resultados_1:
            inicio = text.find(resultado)
            fin = inicio + len(resultado)
            numero_x = Cupon_simple(int(text[inicio+6:fin-1]))
            text = text.replace(text[inicio:fin] ,str(numero_x))
    if len(resultados_2) >0:
        for resultado in resultados_2:
            inicio = text.find(resultado)
            fin = inicio + len(resultado)
            coma = re.search("\,",text[inicio:fin])
            x = text[inicio+6:inicio+coma.start()]
            y = text[inicio+coma.start()+1:fin-1]
            numero_x = Cupon_doble(int(x),int(y))
            text = text.replace(text[inicio:fin] ,str(numero_x))
    r = r'\(( *([0-9]+|ANS) *(\+|\-|\*|\//) *([0-9]+|ANS) *( *(\+|\-|\*|\//) *([0-9]+|ANS) *)?)+\)'
    n_texto = text
    contador = 0
    i = 0
    j = -1
    while contador<len(re.findall(r'\(',text)):
        coincidencias = re.finditer(r, n_texto)
        inicio_fin = [(coincidencia.start(), coincidencia.end()) for coincidencia in coincidencias]
        while i < len(inicio_fin):
            inicio = inicio_fin[j][0]
            fin = inicio_fin[j][1]
            y = str(resolver_problema(n_texto[inicio+1:fin-1])) + " "
            lista_caracteres = list(n_texto)
            lista_caracteres[inicio:fin] = y
            n_texto = "".join(lista_caracteres)
            j -=1
            i +=1
            contador +=1
        i = 0
        j = -1
        n_texto = n_texto
    text = n_texto
    text = text.strip()
    patron = r'( *\+ *| *\- *| *\* *| *\// *)'
    operaciones = re.split(patron, text)
    text = [elemento.strip() for elemento in operaciones if elemento.strip() != '']
    text = resolver_prioridad_1(text)
    text = resolver_prioridad_2(text)
    resultado = int(text[0])
    if resultado < 0:
        resultado = 0
    return resultado

def resolver_bloque(lista_problemas,archivo):
    '''
    ***
    * texto : 
    ***
    describe la funcion
    '''
    flag = True
    lineas_error = []
    for w in lista_problemas:
            if revision_errores(w) == False:
                flag = False
                lineas_error.append(w)
    if flag==True:
        for w in lista_problemas:
            solucion = resolver_problema(w)
            global ans
            ans = solucion
            archivo.write(str(w)+" = "+ str(solucion)+"\n")
        archivo.write("\n")
    else:
        for w in lista_problemas:
            if w in lineas_error:
                archivo.write(str(w)+" = "+ "Error"+"\n")
            else:
                archivo.write(str(w)+" = "+ "Sin Resolver"+"\n")
        archivo.write("\n")

ans = 0
lista_problemas = []
problemas = open("problemas.txt","r") #cambiar nombre de archivo
desarrollo = open("desarrollos.txt","w")
for contenido in problemas:
    lista_problemas.append(contenido.strip())
    if contenido == "\n":
        lista_problemas.pop()
        resolver_bloque(lista_problemas,desarrollo)
        lista_problemas = []
resolver_bloque(lista_problemas,desarrollo)
problemas.close()
desarrollo.close()