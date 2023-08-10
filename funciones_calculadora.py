def suma(a,b):
    s = int(a) + int(b)
    return s

def resta(a,b):
    s = int(a) - int(b)
    return s

def producto(a,b):
    s = int(a) * int(b)
    return s

def division(a,b):  #b != 0 al ser llamada ?
    s = int(a) // int(b)
    return s

def Cupon_simple(x):
    s = int(x) * 0.8
    return int(s)

def Cupon_doble(x,y):
    z = float(y) / 100.0
    s = int(x) * (1-z)
    return int(s)