#!/usr/bin/env python3
import argparse
import collections
import os
import struct
from collections import Counter

from heapq import heappush, heappop, heapify
from collections import defaultdict

MAGIC_NUMBER = 69 # magic number for identification
SIZE_ARR = 6


def forceCierre(txt, contador, args, file):
    if (len(txt) < contador) and not args.force:
        file.close()
        print("El archivo comprimido es mas grande que el original no se comprimio")
        os.remove(args.archivo.name + ".huf")
        raise Exception
    else:
        file.close()
        print("Archivo comprimido exitosamente")



def main():
    parser = argparse.ArgumentParser(
        description='Comprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('archivo', help='archivo a comprimir ',
                        type=argparse.FileType('r'))
    parser.add_argument('-f', '--force', help='forzar la compresión, aunque el archivo resultante sea más grande',
                        required=False, action="store_true")
    parser.add_argument('-v', '--verbose',
                        help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo',
                        required=False, action="store_true")

    args = parser.parse_args()
    file = open(args.archivo.name +".huf", "wb+")
    txt = args.archivo.read()

    symb2freq = collections.Counter(txt)
    huff = encode(symb2freq)

    dicc_symbols,list_symbols=generarDicc(huff,args)

    #Generar el Cabezal del archivo.huf
    cabezal = struct.pack('!hBBi',MAGIC_NUMBER,len(list_symbols),SIZE_ARR,len(txt))

    #Contador nos va a servir para comparar el tamaño del archivo original y el nuevo
    contador=len(cabezal)
    file.write(cabezal)


    encoded_table = generarTablaDeCodigo(huff)

    #Escribir la codificacion en el archivo
    for c in encoded_table:
        for s in c:
           contador = contador + len(s)
           file.write(s)

    #Esccribimos los caracteres del texto con sus codigos en binario
    texto_codificado = ''
    for char in txt:
        texto_codificado+=dicc_symbols[char]

    bites=comprimirTextoCodificado(texto_codificado)
    contador = contador + len(bites)


    #Paso el texto a bytes
    texto_codificado=bytes(bites)
    file.write(texto_codificado)

    try:
        forceCierre(txt,contador,args,file)
    except:
        return -1  # dehuff devuelve -1 y corta el proceso

    return 0


def encode(symb2freq):
    """Huffman encode the given dict mapping symbols to weights"""
    heap = [[wt, [sym, ""]] for sym, wt in symb2freq.items()]
    heapify(heap)
    while len(heap) > 1:
        lo = heappop(heap)
        hi = heappop(heap)
        for pair in lo[1:]:
            pair[1] = '0' + pair[1]
        for pair in hi[1:]:
            pair[1] = '1' + pair[1]
        heappush(heap, [lo[0] + hi[0]] + lo[1:] + hi[1:])
    return sorted(heappop(heap)[1:], key=lambda p: (len(p[-1]), p))


def generarDicc(huff, args):
    '''Genera un diccionario y una lista con los simbolos y su codigo.Ademas se le pasa args  por si se usa verbose para que imprima
    la codificacion en la terminal'''

    dicc_symbols = {p[0]: p[1] for p in huff}  # Estructura que nos va a ayudar para transcribir el texto
    list_symbols = [(p[0], p[1]) for p in huff]  # lista de Caracteres y sus codigos
    if args.verbose:
        print("Caracter / Codigo")
        for tupla in list_symbols:
            print(f'{tupla[0]}   /  {tupla[1]}')
    return dicc_symbols, list_symbols


def generarTablaDeCodigo(huff):
    '''Genera una tabla con los simbolos , el largo del su codigo y su codigo'''
    encoded_table = []
    for p in huff:
        symbol = struct.pack('!B', int(format(ord(p[0]), 'd')))
        code_len = struct.pack('!B', len(p[1]))
        code = struct.pack('!i', int(p[1], 2))
        encoded_table.append([symbol, code_len, code])
    return encoded_table

def comprimirTextoCodificado(texto_codificado):
    '''Agarro el chorizo de 0 y 1  y los separa de a 8 bites, y lo guarda en un vector, si llega a faltar le agrega 0 al final '''
    bites = []
    for i in range(0,len(texto_codificado),8):
        byte=texto_codificado[i:i+8]
        if len(byte)==8:
            bites.append(int(byte,2))
        else:
            byte += (8-len(byte))*'0'
            bites.append(int(byte,2))
        return bites


if __name__ == '__main__':
    main()
