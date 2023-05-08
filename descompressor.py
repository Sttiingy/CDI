import os
import sys
import time
from Huffman import Huffman

start = time.time()
huff = Huffman(sys.argv[1])
output_path = huff.comprimir()
sizefile = os.stat("quijote_clean.cdi").st_size
print("Tamaño archivo comprimido:", sizefile, "Bytes")
print("Num de caracteres unicode original:", len(open(sys.argv[1], "r+").read()))
print("Bits per simbol", (8 * sizefile) / len(open(sys.argv[1], "r+").read()))

end = time.time()

print("Temps total:", end - start)



path = "quijote_clean.txt"
h = Huffman(path)

output_path = h.comprimir()

decom_path = h.decompress(output_path)
