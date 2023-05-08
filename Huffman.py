import sys
import heapq
import os
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

	def make_frequency_dict(self, text):
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


	def makeCodesRec(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codis[root.char] = current_code
			self.reverseMap[current_code] = root.char
			return

		self.makeCodesRec(root.left, current_code + "0")
		self.makeCodesRec(root.right, current_code + "1")


	def makeCodes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.makeCodesRec(root, current_code)


	def ObtenirTextEncoded(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codis[character]
		return encoded_text


	def paddingTextEcoded(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def obtenirByteArray(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			print("Encoded text not padded properly")
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def comprimir(self):
		#Agafo el nom del fitxer per generar el output
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + ".cdi"

        #LLegim el fitxer i definim el output com a wb(Write binary)
		with open(self.path, 'r+') as file, open(output_path, 'wb') as output:
			text = file.read()
			text = text.rstrip()

            #Calculem les frequencies
			frequency = self.make_frequency_dict(text)
			#Fem l'arbre de frequencies
			self.constriurHeap(frequency)
			#Construim l'arbre de nodes de menor frequencia i establim les etiquetes amb la suma de frequencies
			self.construirNodes()
			#Construim els codis per a cada node amb un 0 a l'esquerra i un 1 a la dreta
			self.makeCodes()

            #Obtenim la cadena de 1 i 0 del nostre text d'input
			encoded_text = self.ObtenirTextEncoded(text)

			#Garantitzem que el codi de 1 i 0 és de longitud multiple de 8
			padded_encoded_text = self.paddingTextEcoded(encoded_text)
			
			#construim la byte array corresponent al padded code
			b = self.obtenirByteArray(padded_encoded_text)
			
			output.write(bytes(b))

		return output_path


	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in self.reverse_mapping):
				character = self.reverse_mapping[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, input_path):
		filename, file_extension = os.path.splitext(self.path)
		output_path = filename + "_decompressed" + ".txt"

		with open(input_path, 'rb') as file, open(output_path, 'w') as output:
			bit_string = ""

			byte = file.read(1)
			while(len(byte) > 0):
				byte = ord(byte)
				bits = bin(byte)[2:].rjust(8, '0')
				bit_string += bits
				byte = file.read(1)

			encoded_text = self.remove_padding(bit_string)

			decompressed_text = self.decode_text(encoded_text)
			
			output.write(decompressed_text)

		print("Decompressed")
		return output_path
