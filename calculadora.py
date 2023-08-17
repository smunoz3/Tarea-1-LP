import re

def resolver_prioridad_1(texto):
    '''
    ***
    * texto : Tipo lista
    ***
    Recibe una lista, la recorre de izquierda a derecha 
    y va resolviendo las opereraciones de producto y division
    Retorna una lista sin producto ni division
    '''
    i = 0 

    while i <len(texto):
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
    Recibe una lista la recorre de izquierda a derecha
    y va resolviendo las opereraciones de suma y resta
    Retorna una lista sin suma ni resta
    '''
    i = 0

    while i <len(texto):
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
    Recibe un numero y obtiene su 20%
    Retorna un int, el 20% de x
    '''
    s = int(x) * 0.2

    return int(s)

def Cupon_doble(x,y):
    '''
    ***
    * x : Tipo int
    * y : Tipo int
    ***
    Recibe dos numeros y al primero le obtiene el % del segundo
    Retorna un int, el y% de x
    '''
    z = float(y) / 100.0
    s = int(x) * z

    return int(s)

def validacion_operacion(text):
    '''
    ***
    * text : Tipo string
    ***
    Recibe un string y revisa si antes y despues de las operaciones hay caracteres validos
    Retorna un bool, True si es valido y False si no es valido
    '''
    retorno = True
    operaciones = r'\+|\-|\*|\//'
    valido_1 = ['0','1','2','3','4','5','6','7','8','9','S',')']
    valido_2 = ['0','1','2','3','4','5','6','7','8','9','A','C','(']
    matches = [match.start() for match in re.finditer(operaciones, text)]

    for i in matches:
        try:
            text[i+1]
        except IndexError:
            return False
        if text[i] == "/":
            try:
                text[i+2]
            except IndexError:
                return False
            if not ((text[i-1] in valido_1) and (text[i+2] in valido_2)):
                retorno = False
        elif not ((text[i-1] in valido_1) and (text[i+1] in valido_2)):
            retorno = False

    return retorno

def validacion_cupones(text):
    '''
    ***
    * text : Tipo string
    ***
    Recibe un string y revisa la escritura de los cupones esta bien escrita
    Retorna un bool, True si es valido y False si no es valido
    '''
    if (len(re.findall(r'(CUPON\(CUPON\()|(CUPON\(\))|(CUPON\((\d|ANS),\))|(CUPON\((\d|ANS)\,CUPON\()',text))!=0):
        return False
    if (len(re.findall(r'CUPON\((\d|ANS)(\+|\-|\*|\//)',text)))!=0:
        return False
    
    return True

def revision_errores(text,ans):
    '''
    ***
    * text : Tipo string
    * ans : Tipo int
    ***
    Recibe string, que en cada ANS se reemplza por el int ans,
    y se va validando mediante expreciones regulares,
    tambien llama a validacion_operacion y a validacion_cupones 
    Retorna un bool, True si no hay errores y False si hay errores
    '''
    text = text.replace("ANS",str(ans))
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
    if (len(re.findall(r'\d\(|\)\d|(\+|\-|\*|\//|\d|ANS)\(\d\)', text)) != 0):
        return False
    if (len(re.findall(r'^(\+|\-|\*|\//)\d',text))) !=0:
        return False
    
    if validacion_operacion(text) == False:
        return False
    if validacion_cupones(text) == False:
        return False
    
    text = re.sub(r'(CUPON\([0-9]+\))', str(1), text)
    text = re.sub(r'CUPON\([0-9]+,[0-9]+\)', str(2), text)
    if (len(re.findall(r'[^(\d|\+|\-|\*|\//)]',text))!=0):
        return False

    return True

def resolver_cupon(text):
    '''
    ***
    * text : Tipo string
    ***
    Recibe un string va calculando y reemplazando los cupones  
    Retorna un string, con los cupones ya reemplazados
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

    return text

def resolver_problema(text,ans):
    '''
    ***
    * text : Tipo string
    * ans : Tipo int
    ***
    Recibe string, que en cada ANS se reemplza por el int ans, previamente validado se va resolviendo las operaciones en orden
    primero los CUPONES, despues los () de manera recursiva, 
    luego llama a resolver el producto y division y finalmente llama a resolver suma y resta
    Retorna un int, el resultado de las operaciones, 0 si es menor que 0
    '''
    text = text.replace("ANS",str(ans))
    text = resolver_cupon(text)
    
    r = r'\(( *([0-9]+) *(\+|\-|\*|\//) *([0-9]+) *( *(\+|\-|\*|\//) *([0-9]+) *)?)+\)'
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
            y = str(resolver_problema(n_texto[inicio+1:fin-1],ans)) + " "
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
    * lista_problemas : Tipo lista
    * archivo : Tipo archivo
    ***
    Recibe una lista donde cada indice es una linea de operaciones, primero se ve si tiene errores
    por medio de la funcion revision_errores, si esta bien llama a resolver_problema 
    y escribe en archivo los resultados, si estan mal no resuelve y escribe en el archivo los errores
    Retorna nada
    '''
    flag = True
    lineas_error = []
    ans_temp = 0

    for w in lista_problemas:
            if revision_errores(w,ans_temp) == False:
                flag = False
            elif revision_errores(w,ans_temp)==True:
                ans_temp = resolver_problema(w,ans_temp)
    if flag == False:
        for w in lista_problemas:
            if revision_errores(w,0) == False:
                lineas_error.append(w)

    if flag==True:
        for w in lista_problemas:
            global ans
            solucion = resolver_problema(w,ans)
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
problemas = open("problemas.txt","r")
desarrollo = open("desarrollos.txt","w")

for contenido in problemas:
    lista_problemas.append(contenido.strip())
    if contenido == "\n":
        lista_problemas.pop()
        resolver_bloque(lista_problemas,desarrollo)
        lista_problemas = []
        ans = 0
resolver_bloque(lista_problemas,desarrollo)

problemas.close()
desarrollo.close()