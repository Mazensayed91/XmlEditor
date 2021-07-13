import re
from utils import read_xml, to_json, write_xml
import json

class TrieNode:
    def __init__(self, freq, symbol, left=None, right=None):
        self.freq = freq

        self.symbol = symbol

        self.left = left

        self.right = right

        self.huff = ''


def min_compress(xml):
    return re.sub("</.*?>", "&", xml)


def huffman_compress(xml):
    freq = build_freq_dictionary(xml)
    trie_nodes = []
    for key, value in freq.items():
        trie_nodes.append(TrieNode(value, key))

    while len(trie_nodes) > 1:
        trie_nodes = sorted(trie_nodes, key=lambda x: x.freq)

        left = trie_nodes[0]
        right = trie_nodes[1]
        left.huff = 0
        right.huff = 1

        new_node = TrieNode(left.freq + right.freq, left.symbol + right.symbol, left, right)

        trie_nodes.remove(left)
        trie_nodes.remove(right)
        trie_nodes.append(new_node)

    return printNodes(trie_nodes[0]), freq


def build_freq_dictionary(xml):
    freq = {}

    for char in xml:
        freq[char] = freq.get(char, 0) + 1

    return freq


dic = {}


def printNodes(node, val=''):
        # huffman code for current node
        newVal = val + str(node.huff)

        # if node is not an edge node
        # then traverse inside it
        if node.left:
            printNodes(node.left, newVal)
        if node.right:
            printNodes(node.right, newVal)

            # if node is edge node then
            # display its huffman code
        if not node.left and not node.right:
            dic[node.symbol] = newVal
            # print(f"{node.symbol} -> {newVal}")
        return dic


def encode(xml_data):
    #binary_file = open(path, "w")
    binary_huffman_tree, freq = huffman_compress(xml_data)
    with open('tree.txt', 'w') as convert_file:
     convert_file.write(json.dumps(binary_huffman_tree))
    print(binary_huffman_tree)
    big_text = ""
    big_text2 = ""
    encoded_xml = ""
    for char in xml_data:
        big_text += binary_huffman_tree[char]
        big_text2 += binary_huffman_tree[char]
        if len(big_text) >=7:
            encoded_xml += chr(int(big_text[:7], 2))
            big_text = big_text[7:]
    # if len(big_text) != 0:
    #     encoded_xml += chr(int(big_text, 2))
    print(big_text2)
    print("\char encoded:\n")
    print(encoded_xml)
    return encoded_xml

        # if len(big_text) >= 7:
        #     character = big_text[:7]
        #     big_text = big_text[7:]
        #     character = int('0b' + character, 2)
        #     binary_char = character.to_bytes((character.bit_length() + 7) // 8, 'big').decode()
        #     small_text += binary_char
        #     binary_file.write(binary_char)

    # binary_int = int(big_text, 2)
    # byte_number = binary_int.bit_length() + 7 // 8
    # binary_array = binary_int.to_bytes(byte_number, "big")
    # ascii_text = binary_array.decode()
    # print(ascii_text)
    #print(big_text)

    # to_json(freq, "freq")
    #binary_file.close()


def decode(path):
    binary_file = open(path, "r")
    encoded_data = binary_file.read()
    # decoded_xml = ""
    input_string = bin(int.from_bytes(encoded_data.encode(), 'big'))[2::]
    # for char in encoded_data:
    #     decoded_xml += bin(ord(char))[2::]
    for i in range(1, len(input_string)):
        if i%7 == 0:
            input_string = input_string[:i] + input_string[i+1::]

    with open('tree.txt') as f:
        data = f.read()
    tree = json.loads(data)
    chars = list(tree.keys())
    freq = list(tree.values())
    decode_huffman(input_string, chars, freq)
    print("\nbinary decoded:\n")
    print(input_string)
    return input_string

def decode_huffman(input_string,  char_store, freq_store):
    #input_string Huffman encoding
    #char_store character set 
    #freq_store Character transcoding 01 sequence
    encode = ''
    decode = ''
    for index in range(len(input_string)):
        encode = encode + input_string[index]
        for item in zip(char_store, freq_store):
            if encode == item[1]:
                decode = decode + item[0]
                encode = ''
    print(decode)
    return decode; 
