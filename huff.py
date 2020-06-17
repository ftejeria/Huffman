import argparse


def main():
    parser = argparse.ArgumentParser(description='Comprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('-f', '--froce', help='forzar la compresión, aunque el archivo resultante sea más grande', required=False, type=str)
    parser.add_argument('-v', '--verbose', help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo', required=False, type=str)
    args = parser.parse_args()

    huff(args)

def huff(args):
    print("hola")

if __name__ == '__main__':
    main()
