import heapq
import os
import time

class Node:
    prob = 0.0
    symbol = ""
    encoding = ""
    visited = False
    parent = -1

class Huffman:
    tree = None
    root = None
    nodes = []
    probs = {}
    dictEnder = {}

    def __init__(self, symbols):
        self.initNodes(symbols)
        self.buildTree()
        self.buildDictionary()

    def initNodes(self, probs):
        for symbol in probs:
            node = Node()
            node.symbol = symbol
            node.prob = probs[symbol]
            node.visited = False
            self.nodes.append(node)
            self.probs[symbol] = probs[symbol]

    def buildTree(self):
        indexMin1 = self.getNodeWithMinimumProb()
        indexMin2 = self.getNodeWithMinimumProb()

        while indexMin1 != -1 and indexMin2 != -1:
            node = Node()
            node.symbol = "."
            node.encoding = ""
            prob1 = self.nodes[indexMin1].prob
            prob2 = self.nodes[indexMin2].prob
            node.prob = prob1 + prob2
            node.visited = False
            node.parent = -1
            self.nodes.append(node)
            self.nodes[indexMin1].parent = len(self.nodes) - 1
            self.nodes[indexMin2].parent = len(self.nodes) - 1

            if(prob1 >= prob2):
                self.nodes[indexMin1].encoding = "0"
                self.nodes[indexMin2].encoding = "1"
            else:
                self.nodes[indexMin1].encoding = "1"
                self.nodes[indexMin2].encoding = "0"
            indexMin1 = self.getNodeWithMinimumProb()
            indexMin2 = self.getNodeWithMinimumProb()

    def getNodeWithMinimumProb(self):
        minProb = 1.0
        indexMin = -1

        for index in range(0, len(self.nodes)):
            if(self.nodes[index].prob < minProb and (not self.nodes[index].visited)):
                minProb = self.nodes[index].prob
                indexMin = index

        if indexMin != -1:
            self.nodes[indexMin].visited = True
        return indexMin
    
    def showSymbolEncoding(self, symbol):
        found = False
        index = 0
        encoding = ""

        for i in range(0, len(self.nodes)):
            if self.nodes[i].symbol == symbol:
                found = True
                index = i
                break

        if found:
            while index != -1:
                encoding = "%s%s" % (self.nodes[index].encoding, encoding)
                index = self.nodes[index].parent
        else:
            encoding = "Not found"

        return encoding
    
    def buildDictionary(self):
        for symbol in self.probs:
            encoding = self.showSymbolEncoding(symbol)
            self.dictEnder[symbol] = encoding

    def encode(self, plain):
        encoded = ""
        for symbol in plain:
            encoded = "%s%s" % (encoded, self.dictEnder[symbol])

        return encoded

start = time.time()
input = open("pruebas.txt").read()
simbolos = ''
probabilidad = []
msg = input

for i in input:
    if i in msg:
        simbolos += i
        probabilidad.append(float(float(msg.count(i))/ float(len(msg))))
        msg = msg.replace(i,'')
symbols = dict(zip(simbolos, probabilidad))

print(len(input))


huffman = Huffman(symbols)
encode = huffman.encode(input)

with open('code.txt', 'w') as f:
    f.write(encode)
end = time.time()
print("Temps compressió: ", end - start)