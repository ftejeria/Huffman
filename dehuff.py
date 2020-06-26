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
    nombreArchivo = args.archivo.name
    vecNombre=nombreArchivo.split('.')
    if (vecNombre[-1] != "huf"):
        print("El archivo no es del formato '.huf' , no se puede descomprimir")
        return 0
    txt=args.archivo.read()

    parteNombre=''
    for i in range(len(vecNombre)-1):
        parteNombre+=vecNombre[i]
    file=open(parteNombre+".ori","w")

    #print(txt[:2])  # numero magico
    #print(txt[2:3])  # cantidad de simbolos que hay
    #print(txt[3:4])  # tamañano de cada simbolo (6)
    #print(txt[4:8])  # largo del archivo original

    cabezal = struct.unpack('!hBBi', txt[:8])
    dic_codificacion={}

    if args.verbose:
        print("Caracter / Codigo")
    for i in range(8,8+cabezal[1]*cabezal[2],cabezal[2]):
        tuplaCodigo=struct.unpack('!BBi',txt[i:i+cabezal[2]])
        numeroBin='{0:b}'.format(tuplaCodigo[2]) # escribe en binario de la forma mas corta
        parteDeCeros=''
        for _ in range(tuplaCodigo[1]-len(numeroBin)):
            parteDeCeros+='0'
        clave=str(parteDeCeros+numeroBin)
        if args.verbose:
            print(f'"{chr(tuplaCodigo[0])}"  /  {clave}')
        dic_codificacion[clave]=chr(tuplaCodigo[0])


    textobinario=''

    for j in range(8+cabezal[1]*cabezal[2],len(txt)):#leo de a bite y lo guardo como 0 y 1 en un string
        parteDeCeros = ''
        binario=bin(txt[j])[2:] #txt j ya da el numerno en int
        for _ in range(8-len(binario)):
            parteDeCeros+='0'
        binario = parteDeCeros + binario
        textobinario+=binario

    bitsacumulado = 0
    
    for num in range(len(textobinario)):
        if textobinario[num-bitsacumulado:num+1] not in dic_codificacion:
            bitsacumulado+=1
        else:
            file.write(dic_codificacion[textobinario[num-bitsacumulado:num+1]])
            bitsacumulado=0


    file.close()
    



     #decodificar y copiar el texto que queda (lo da el cabezal)



if __name__ == '__main__':
    main()