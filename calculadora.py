import re

flag = True
ANS = 0
lineas_error = []
lista_problemas = []
""" 
def suma(a,b):
    s = int(a) + int(b)
    return s

def resta(a,b):
    s = int(a) - int(b)
    return s

def producto(a,b):
    s = int(a) * int(b)
    return s

def division(a,b):  #b != 0 en revision error
    s = int(a) // int(b)
    return s
 """
def list_to_str(lista):
    string = ""
    i = 0
    while lista[i] != lista[-1]:
        string=string + lista[i] + " "
        i += 1
    string=string + lista[i]
    return string

def resolver_prioridad_1(texto): #resuelve operaciones "*" y "//" en texto 
    i = 0   #texto llega .split()
    while texto[i] != texto[-1]:
        if texto[i] == "ANS":
            texto[i]= str(ANS)
        if texto[i+1] == "ANS":
            texto[i+1]= str(ANS)
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


def resolver_prioridad_2(texto): #resuelve operaciones "+" y "-" en texto 
    i = 0
    while texto[i] != texto[-1]:
        if texto[i] == "ANS":
            texto[i]= str(ANS)
        if texto[i+1] == "ANS":
            texto[i+1]= str(ANS)
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
    s = int(x) * 0.2
    return int(s)

def Cupon_doble(x,y):
    z = float(y) / 100.0
    s = int(x) * z
    return int(s)

def validacion_operacion(texto): #llega sin ""
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
    text = re.sub(r'\s+', '', text) #elimina espacios
    retorno = True
    contador=0
    for i in text:
        if i == "(":
            contador +=1
        if i == ")":
            contador -=1
        if contador <0:
            retorno = False
    if contador != 0:
        retorno = False
    # if len(re.findall("\(", text)) != len(re.findall("\)", text)):
    #     retorno = False
    if len(re.findall("\/0", text)) != 0:
        retorno = False
    if validacion_operacion(text) == False:
        retorno = False
    if len(re.findall(r'[0-9]+\(', text)) != 0:
        retorno = False
    return retorno

def resolver_problema(text):
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
    #o = 0
    n_texto = text
    contador = 0
    i = 0
    j = -1
    temp = len(re.findall(r'\(',text))
    while contador<len(re.findall(r'\(',text)):

        coincidencias = re.finditer(r, n_texto)
        inicio_fin = [(coincidencia.start(), coincidencia.end()) for coincidencia in coincidencias]

        while i < len(inicio_fin):
            inicio = inicio_fin[j][0]
            fin = inicio_fin[j][1]
            y = str(resolver_problema(n_texto[inicio+1:fin-1])) + " "
            #o = o - len(y)
            lista_caracteres = list(n_texto)
            lista_caracteres[inicio:fin + 1] = y
            n_texto = "".join(lista_caracteres)
            j -=1
            i +=1
            contador +=1
        i = 0
        j = -1
        n_texto = n_texto
        
    text = n_texto
    text = text.strip().split()

    #resolver ()

    text = resolver_prioridad_1(text) #text llega .split() y sin "(" ")"
    text = resolver_prioridad_2(text)
    resultado = int(text[0])
    if resultado < 0:
        resultado = 0
    return resultado

problemas = open("problemas (EJEMPLO).txt","r") #cambiar nombre de archivo
desarrollo = open("desarrollos.txt","w")
for contenido in problemas:
    lista_problemas.append(contenido.strip())
    if contenido == "\n":
        lista_problemas.pop() #eliminar '' final
        for w in lista_problemas: # se revisa si hay errores
            if revision_errores(w) == False:
                flag = False
                lineas_error.append(w)
        if flag==True:
            for w in lista_problemas:
                solucion = resolver_problema(w)
                ANS = solucion
                desarrollo.write(str(w)+" = "+ str(solucion)+"\n")
            lista_problemas = []
            desarrollo.write("\n")
        else: #flag == False
            for w in lista_problemas:
                if w in lineas_error:
                    desarrollo.write(str(w)+" = "+ "Error"+"\n")
                else:
                    desarrollo.write(str(w)+" = "+ "Sin resolver"+"\n")
            lista_problemas = []
            desarrollo.write("\n")
            flag = True
            lineas_error = []

for w in lista_problemas: # se revisa si hay errores
    if revision_errores(w) == False:
        flag = False
        lineas_error = w
if flag==True:
    for w in lista_problemas:
        solucion = resolver_problema(w)
        ANS = solucion
        desarrollo.write(str(w)+" = "+ str(solucion)+"\n")
    lista_problemas = []
else: #flag == False
    for w in lista_problemas:
        if w == lineas_error:
            desarrollo.write(str(w)+" = "+ "Error"+"\n")
        else:
            desarrollo.write(str(w)+" = "+ "Sin resolver"+"\n")
    lista_problemas = []
    flag = True
    lineas_error = ""

problemas.close()
desarrollo.close()