from lexAnalyzer import lexerAritmetico
import timeit

O = ['Suma', 'Resta', 'Multiplicacion', 'Division', 'Potencia', 'Asignacion']


def tokenSintax(tokens):
    count = 0
    for token in tokens:
        if token == '(':
            count += 1
        elif token == ')':
            count -= 1
        if count != 0:
            return False
        else: return True

def stateMachine(currentState, token):

    # q0

    if currentState == 'q0':
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real':
            return 'q1'
        elif token[1] == 'Parentesis que abre':
            return 'q3'
        elif token[1] == 'Comentario':
            return 'q7'
        elif token[1] == 'Enter':
            return 'q0'
        elif token[1] in O or token[1] == 'Parentesis que cierra':
            return 'q8'
        else: return 'qError'

    # q1

    if currentState == 'q1':
        if token[1] in O:
            return 'q2'
        if token[1] == 'Parentesis que abre':
            return 'q3'
        if token[1] == 'Comentario':
            return 'q7'
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real' or token[1] == 'Parentesis que cierra':
            return 'q8'
        if token[1] == 'Enter':
            return 'q0'
        else: return 'qError'

    # q2

    if currentState == 'q2':
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real':
            return 'q1'
        elif token[1] == 'Parentesis que abre':
            return 'q3'
        elif token[1] == 'Comentario' or token[1] == 'Parentesis que cierra' or token[1] in O or token[1] == 'Enter':
            return 'q8'
        else: return 'qError'
    
    # q3

    if currentState == 'q3':
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real':
            return 'q4'
        elif token[1] == 'Parentesis que abre' or token[1] == 'Comentario' or token[1] in O or token[1] == 'Enter':
            return 'q8'
        elif token[1] == 'Parentesis que cierra':
            return 'q0'
        else: return 'qError'
    
    # q4

    if currentState == 'q4':
        if token[1] in O:
            return 'q6'
        elif token[1] == 'Parentesis que cierra':
            return 'q5'
        if token[1] == 'Parentesis que abre':
            return 'q8'
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real' or token[1] == 'Parentesis que abre' or token[1] == 'Comentario' or token[1] == 'Enter':
            return 'q8'
        else: return 'qError'

    # q5

    if currentState == 'q5':
        if token[1] in O:
            return 'q2'
        elif token[1] == 'Comentario':
            return 'q7'
        elif token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real' or token[1] == 'Parentesis que abre' or token[1] == 'Parentesis que cierra':
            return 'q8'
        elif token[1] == 'Enter':
            return 'q0'
        else: return 'qError'

    # q6

    if currentState == 'q6':
        if token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real':
            return 'q4'
        elif token[1] == 'Parentesis que abre' or token[1] == 'Parentesis que cierra' or token[1] == 'Comentario' or token[1] == 'Enter' or token[1] in O:
            return 'q8'
        else: return 'qError'

    # q7

    if currentState == 'q7':
        if token[1] == 'Enter':
            return 'q0'
        elif token[1] == 'Variable' or token[1] == 'Entero' or token[1] == 'Real' or token[1] == 'Parentesis que abre' or token[1] == 'Parentesis que cierra' or token[1] == 'Comentario' or token[1] in O:
            return 'q7'
        else: return 'qError'

    # q8

    if currentState == 'q8':
        return 'qError'

    else: return 'qError'


def main():
    start = timeit.default_timer()

    with open('input4.txt', 'r') as archivo:
        expresiones = archivo.readlines()
    
    css = open('style.css', 'w')
    css.write(".mainDiv {display: flex;flex-direction: row;justify-content: space-around;} h1 {color: white;}")
    css.close()

    if tokenSintax(expresiones) == False:
        print('Error de sintaxis')
        exit()

    tokens = lexerAritmetico(expresiones)

    current_state = 'q0'

    f = open('export.html','w')

    f.write('<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0"><title>act3.4</title><link rel="stylesheet" href="style.css"></head></html><body style="background-color: #3E3E3E;"><div class="mainDiv"><div><h1>Proceso de AFD</h1>')


    for token in tokens:

        current_state = stateMachine(current_state, token)
        if current_state == 'qError':
            print('Expresión no válida', current_state )
            f.write('<div style="color: red;"')
            f.write('><p>Expresión no válida ')
            f.write(current_state)
            f.write('</p></div>')
            break
        elif current_state != 'qError':
            print('Expresión válida', current_state)
            f.write('<div style="color: green;"')
            f.write('><p>Expresión válida ')
            f.write(current_state)
            f.write('</p></div>')
        else: 
            print('Expresión válida', current_state)
    f.write('</div><div><h1>Resultado</h1>')


    for token, tipo in tokens:
        if current_state == 'qError':
            break
        if tipo == 'Error':
            f.write(' <div style="color: red;"')
        elif tipo == 'Comentario':
            f.write(' <div style="color: green;"')
        elif tipo == 'Variable':
            f.write(' <div style="color: blue;"')
        elif tipo == 'Entero':
            f.write(' <div style="color: orange;"')  
        elif tipo == 'Real':
            f.write(' <div style="color: purple;"')
        elif tipo == 'Suma':
            f.write(' <div style="color: yellow;"')
        elif tipo == 'Resta':
            f.write(' <div style="color: pink;"')
        elif tipo == 'Multiplicacion':
            f.write(' <div style="color: brown;"')
        elif tipo == 'Division':
            f.write(' <div style="color: cyan;"')
        elif tipo == 'Potencia':
            f.write(' <div style="color: gray;"')
        elif tipo == 'Parentesis que abre':
            f.write(' <div style="color: #33FFC4 ;"')
        elif tipo == 'Parentesis que cierra':
            f.write(' <div style="color: #A8FF33;"')
        elif tipo == 'Asignacion':
            f.write(' <div style="color: magenta;"')
        else: f.write(' <div style="color: white;"')

        if tipo == 'Enter':
            f.write('></div>')
        else:            
            f.write(f'><p>{token} es de tipo {tipo}</p></div>')
        if token == len(tokens) - 1:
            f.write('></div>')
            break
     
    f.write('</div></body>')
    
    f.close()
    
    stop = timeit.default_timer()
    print('Tiempo de ejecucion: ', stop - start)

main()