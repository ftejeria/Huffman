#!/usr/bin/env python3
import argparse
import collections
import os
import struct
from collections import Counter

from heapq import heappush, heappop, heapify
from collections import defaultdict

MAGIC_NUMBER = 69# magic number for identification
SIZE_ARR = 6


def main():
    archivo = 'prueba'
    parser = argparse.ArgumentParser(
        description='Comprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('-a', '--archivo', help='archivo a comprimir ', required=False,
                        type=argparse.FileType('r'))  # por mientras queda false para poder correr
    parser.add_argument('-f', '--froce', help='forzar la compresión, aunque el archivo resultante sea más grande',
                        required=False, type=str)
    parser.add_argument('-v', '--verbose',
                        help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo',
                        required=False, type=str)

    args = parser.parse_args()
    file = open("archivo.huf", "wb+")
    txt = args.archivo.read()
    symb2freq = collections.Counter(txt)
    huff = encode(symb2freq)
    dicc_symbols={p[0]:p[1] for p in huff } # Estructura que nos va a ayudar para transcribir el texto
    list_symbols=[(p[0],p[1]) for p in huff] #lista de Caracteres y sus codigos
    if args.verbose:
        print("Caracter / Codigo")
        for tupla in list_symbols:
            print(f'{tupla[0]}   /  {tupla[1]}')
    cabezal = struct.pack('!hBBi',MAGIC_NUMBER,len(list_symbols),SIZE_ARR,len(txt)) #TODO ARREGLAR EL EMA DE QUE USA MENOS BITES
    file.write(cabezal)

    encoded_table = []
    for p in huff:
        symbol = struct.pack('!B', int(format(ord(p[0]), 'd')))
        code_len = struct.pack('!B', len(p[1]))
        code = struct.pack('!L', int(p[1], 2))
        encoded_table.append([symbol, code_len, code])



    for c in encoded_table:
        for s in c:
           file.write(s)


    texto_codificado = ''
    bites=[]
    for char in txt:
        texto_codificado+=dicc_symbols[char]
    for i in range(0,len(texto_codificado),8):
        byte=texto_codificado[i:i+8]
        if len(byte)==8:
            bites.append(int(byte,2))
        else:
            byte += (8-len(byte))*'0'
            bites.append(int(byte,2))
    texto_codificado=bytes(bites)
    file.write(texto_codificado)
    file.close()



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

if __name__ == '__main__':
    main()
