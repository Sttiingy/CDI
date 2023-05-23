import sys
import os
import heapq
import time

class Huffman:
	def __init__(self, path):
		self.path = path
		self.heap = []
		self.codis = {}
		self.reverseMap = {}

	class Node:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, self)):
				return False
			return self.freq == other.freq

	# functions for compression:

	def obtenirDiccionariFreqs(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def constriurHeap(self, frequency):
		for key in frequency:
			node = self.Node(key, frequency[key])
			heapq.heappush(self.heap, node)

	def construirNodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.Node(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def construirCodesRec(self, root, currentCode):
		if(root == None):
			return

		if(root.char != None):
			self.codis[root.char] = currentCode
			self.reverseMap[currentCode] = root.char
			return

		self.construirCodesRec(root.left, currentCode + "0")
		self.construirCodesRec(root.right, currentCode + "1")


	def makeCodes(self):
		root = heapq.heappop(self.heap)
		currentCode = ""
		self.construirCodesRec(root, currentCode)


	def ObtenirTextEncoded(self, text):
		encodedText = ""
		for character in text:
			encodedText += self.codis[character]
		return encodedText


	def paddingTextEncoded(self, encodedText):
		extraPadding = 8 - len(encodedText) % 8
		for i in range(extraPadding):
			encodedText += "0"

		paddedInfo = "{0:08b}".format(extraPadding)
		encodedText = paddedInfo + encodedText
		return encodedText


	def obtenirByteArray(self, paddedEncodedText):
		if(len(paddedEncodedText) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(paddedEncodedText), 8):
			byte = paddedEncodedText[i:i+8]
			b.append(int(byte, 2))
		return b


	def comprimir(self):
		#Agafo el nom del fitxer per generar el output
		filename, fileExtension = os.path.splitext(self.path)
		outputPath = filename + ".cdi"

        #LLegim el fitxer i definim el output com a wb(Write binary)
		with open(self.path, encoding="utf8") as file, open(outputPath, 'wb') as output:
			text = file.read()
			text = text.rstrip()

            #Calculem les frequencies
			frequency = self.obtenirDiccionariFreqs(text)
			#Fem l'arbre de frequencies
			self.constriurHeap(frequency)
			#Construim l'arbre de nodes de menor frequencia i establim les etiquetes amb la suma de frequencies
			self.construirNodes()
			#Construim els codis per a cada node amb un 0 a l'esquerra i un 1 a la dreta
			self.makeCodes()

            #Obtenim la cadena de 1 i 0 del nostre text d'input
			encodedText = self.ObtenirTextEncoded(text)

			#Garantitzem que el codi de 1 i 0 és de longitud multiple de 8
			paddedEncodedText = self.paddingTextEncoded(encodedText)
			
			#construim la byte array corresponent al padded code
			b = self.obtenirByteArray(paddedEncodedText)
			
			output.write(bytes(b))

		return outputPath


	def removePadding(self, paddedEncodedText):
		paddedInfo = paddedEncodedText[:8]
		extraPadding = int(paddedInfo, 2)

		paddedEncodedText = paddedEncodedText[8:] 
		encodedText = paddedEncodedText[:-1*extraPadding]

		return encodedText

	def decodeText(self, encodedText):
		currentCode = ""
		decodedText = ""

		for bit in encodedText:
			currentCode += bit
			if(currentCode in self.reverseMap):
				character = self.reverseMap[currentCode]
				decodedText += character
				currentCode = ""

		return decodedText


	def decompress(self, inputPath):
		filename, fileExtension = os.path.splitext(self.path)
		outputPath = filename + "-desc" + ".txt"

		with open(inputPath, 'rb') as file, open(outputPath, 'w', encoding="utf-8") as output:
			bitString = ""

			byte = file.read(1)
			print(byte)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bitString += bits
				byte = file.read(1)

			encodedText = self.removePadding(bitString)

			decompressedText = self.decodeText(encodedText)
			
			output.write(decompressedText)

		return outputPath

start = time.time()
fileName = sys.argv[1] + '.txt'
fileDecompress = sys.argv[1] + '.cdi'
if os.name == 'nt': #si estem a windows hem d'afegir .\ per al nom del fitxer
    fileName = ".\\" + fileName
    fileDecompress = ".\\" + fileDecompress

huff = Huffman(fileName)
outputPath = huff.comprimir()
huff.decompress(fileDecompress)

end = time.time()

print("Temps descompressió =", end - start)
