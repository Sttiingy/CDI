import heapq
import os
import time


def build_huffman_tree(freq_dict):
    heap = []
    for char, freq in freq_dict.items():
        heapq.heappush(heap, (freq, char))
    heap1 = []
    while len(heap) > 1:
        freq1, char1 = heapq.heappop(heap)
        freq2, char2 = heapq.heappop(heap)
        merged_freq = freq1 + freq2
        merged_char = None
        merged_node = (merged_freq, merged_char, (freq1, char1), (freq2, char2))
        heapq.heappush(heap1, merged_node)
    return heap1[0]


def build_code_table(node, code='', code_table={}):
    if len(node) === 4
        freq, char, left, right = node
    else: 
        
    if char:
        code_table[char] = code
    else:
        build_code_table(left, code + '0', code_table)
        build_code_table(right, code + '1', code_table)
    return code_table


def compress(input_file, output_file):
    # Read input file and calculate character frequencies
    with open(input_file, 'r') as f:
        content = f.read()
    freq_dict = {}
    for char in content:
        freq_dict[char] = freq_dict.get(char, 0) + 1

    # Build Huffman tree and code table
    root_node = build_huffman_tree(freq_dict)
    code_table = build_code_table(root_node)

    # Compress file and write to output file
    with open(output_file, 'wb') as f:
        bit_string = ''
        for char in content:
            bit_string += code_table[char]
        # Pad bit string with zeros to make its length a multiple of 8
        padding = 8 - len(bit_string) % 8
        bit_string += '0' * padding
        # Convert bit string to bytes and write to file
        byte_string = bytes([int(bit_string[i:i+8], 2) for i in range(0, len(bit_string), 8)])
        f.write(byte_string)

    # Calculate bits per symbol and compression time
    bits_per_symbol = sum(freq_dict[char] * len(code_table[char]) for char in freq_dict) / len(content)
    start_time = time.time()
    compress(input_file, output_file)
    end_time = time.time()
    compression_time = end_time - start_time

    # Print results
    print(f'Bits per symbol: {bits_per_symbol:.2f}')
    print(f'Compression time: {compression_time:.2f} seconds')

input = "quijote_clean.txt"
compress(input, "output")
