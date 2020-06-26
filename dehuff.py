#!/usr/bin/env python3
import argparse
import collections
import struct

MAGIC_NUMBER = 69




def main():
    parser = argparse.ArgumentParser(description='Descomprimir archivos usando un árbol de Huffman ')  # generamos objeto parser y le damos una descripcion
    parser.add_argument('-v', '--verbose', help='escribe en stderr información sobre el avance del proceso,por ejemplo, los bitcodes para cada símbolo', required=False,action="store_true")
    parser.add_argument('archivo', help='archivo a descomprimir ',
                        type=argparse.FileType('rb'))
    args = parser.parse_args()


    try:
       txt,vecNombre=verificarArchivo(args)
    except:
        return -1 #dehuff devuelve -1 y corta el proceso



    parteNombre=''
    for i in range(len(vecNombre)-1):
        parteNombre+=vecNombre[i]
    file=open(parteNombre+".ori","w")


    cabezal = struct.unpack('!hBBi', txt[:8])



    dic_codificacion={}
    generarDiccionario(args,txt,dic_codificacion,cabezal)

    textobinario=''
    textobinario=generarTextoEnBinario(textobinario,cabezal,txt)

    decodificarTexto(textobinario,dic_codificacion,file)
    file.close()
    print("Archivo descomprimido exitosamente")
    return 0

def verificarArchivo(args):
    '''Verifica que el archivo sea un archivo.huf'''
    nombreArchivo = args.archivo.name
    vecNombre = nombreArchivo.split('.')
    if (vecNombre[-1] != "huf"):
        print("El archivo no es del formato '.huf' , no se puede descomprimir")
        raise Exception
    return args.archivo.read(),vecNombre

def generarDiccionario(args,txt,dic_codificacion,cabezal):
    '''Esta funcion sirve para generar un diccionario que contega el codigo en binario de los caracteres del archivo como key y el valor sera
    ser el caracter en si.Se le pasa demas args para usar el args.versbose y asi imprimir el simbolo y el codigo a la vez que se crea el diccionario,
    de esta manera se hace eficientemente.'''
    if args.verbose:
        print("Caracter / Codigo")
    for i in range(8, 8 + cabezal[1] * cabezal[2], cabezal[2]):
        tuplaCodigo = struct.unpack('!BBi', txt[i:i + cabezal[2]])
        numeroBin = '{0:b}'.format(tuplaCodigo[2])  # escribe en binario de la forma mas corta
        parteDeCeros = ''
        for _ in range(tuplaCodigo[1] - len(numeroBin)):
            parteDeCeros += '0'
        clave = str(parteDeCeros + numeroBin)
        if args.verbose:
            print(f'"{chr(tuplaCodigo[0])}"  /  {clave}')
        dic_codificacion[clave] = chr(tuplaCodigo[0])



def generarTextoEnBinario(textobinario, cabezal, txt):
    '''Se pasa el texto del archivo original de bites a binario '''
    for j in range(8 + cabezal[1] * cabezal[2], len(txt)):  # leo de a bite y lo guardo como 0 y 1 en un string
        parteDeCeros = ''
        binario = bin(txt[j])[2:]  # txt j ya da el numerno en int
        for _ in range(8 - len(binario)):
            parteDeCeros += '0'
        binario = parteDeCeros + binario
        textobinario += binario
    return textobinario


def decodificarTexto(textobinario, dic_codificacion,file):
    '''Se decodifica el texto binario usando el diccionario y a su vez se va escribiendo en el archivo.ori'''
    bitsacumulado = 0
    for num in range(len(textobinario)):
        if textobinario[num - bitsacumulado:num + 1] not in dic_codificacion:
            bitsacumulado += 1
        else:
            file.write(dic_codificacion[textobinario[num - bitsacumulado:num + 1]])
            bitsacumulado = 0




if __name__ == '__main__':
    main()