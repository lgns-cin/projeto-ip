import random as rd

def gerar_y_coletaveis():
    lista_y = []

    while True:
        y_arbitrario = rd.randint(50, 550)

        if not lista_y:
            lista_y.append(y_arbitrario)
        else:
            while True:
                for i in lista_y:
                    # Check if the new y position is too close to any existing y position
                    if y_arbitrario in range(i - 70, i + 70):
                        while y_arbitrario in range(i - 70, i + 70):
                            y_arbitrario = rd.randint(80, 520)

                    contador2 = 0
                    for j in lista_y:
                        if y_arbitrario not in range(j - 70, j + 70):
                            contador2 += 1
                            
                    if contador2 == len(lista_y):
                        if (len(lista_y) < 4) and (y_arbitrario in range(50, 550)):
                            lista_y.append(y_arbitrario)

                if len(lista_y) == 4:
                    break

        if len(lista_y) == 4:
            break

    return lista_y