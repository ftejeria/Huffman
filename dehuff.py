#!/usr/bin/env python3
import argparse


def main():
    parser = argparse.ArgumentParser(description='Descomprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('-v', '--verbose', help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo', required=False, type=str)
    args = parser.parse_args()

    dehuff(args)

def dehuff(args):
    print("hola")

if __name__ == '__main__':
    main()