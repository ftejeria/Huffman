#!/usr/bin/env python3
import argparse
from collections import Counter

from heapq import heappush, heappop, heapify
from collections import defaultdict

def main():
    parser = argparse.ArgumentParser(description='Comprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('-a', '--archivo',help ='archivo a comprimir ',  required=False, type=argparse.FileType('r')) #por mientras queda false para poder correr
    parser.add_argument('-f', '--froce', help='forzar la compresión, aunque el archivo resultante sea más grande', required=False, type=str)
    parser.add_argument('-v', '--verbose', help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo', required=False, type=str)

    args = parser.parse_args()

    txt = "hola como estas"
    symb2freq = defaultdict(int)
    for ch in txt:
        symb2freq[ch] += 1
    # in Python 3.1+:
    # symb2freq = collections.Counter(txt)
    huff = encode(symb2freq)
    print("Symbol\tWeight\tHuffman Code")
    for p in huff:
        print( "%s\t%s\t%s" % (p[0], symb2freq[p[0]], p[1]))



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
