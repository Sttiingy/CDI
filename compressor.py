import sys
import os
import time
from Huffman import Huffman
	

start = time.time()
fileName = sys.argv[1] + '.txt'
fileDecompress = sys.argv[1] + '.cdi'
if os.name == 'nt': #si estem a windows hem d'afegir .\ per al nom del fitxer
    fileName = ".\\" + fileName
    fileDecompress = ".\\" + fileDecompress

huff = Huffman(fileName)
output_path = huff.comprimir()
sizefile = os.stat(fileDecompress).st_size
print("Tamaño archivo comprimido:", sizefile, "Bytes")
print("Num de caracteres unicode original:", len(open(fileName, "r+").read()))
print("Bits per simbol", (8 * sizefile) / len(open(fileName, "r+").read()))

end = time.time()

print("Temps total:", end - start)



