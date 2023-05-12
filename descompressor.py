import os
import sys
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
huff.decompress(fileDecompress)
# sizefile = os.stat(fileDecompress).st_size

end = time.time()

print("Temps total:", end - start)
