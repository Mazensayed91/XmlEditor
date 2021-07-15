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
    binary_huffman_tree, freq = huffman_compress(xml_data)
    # with open(path+'tree.txt', 'w') as convert_file:
        # convert_file.write(json.dumps(binary_huffman_tree))
    tree = json.dumps(binary_huffman_tree)
    big_text = ""
    encoded_xml = ""
    for char in xml_data:
        big_text += binary_huffman_tree[char]
    for i in range(0, len(big_text), 8):
        encoded_xml+=(chr(int(big_text[i:i + 8], 2)))
    return ''.join([tree, encoded_xml])


def decode(path):
    encoded_data = read_xml(path)
    tree = ""
    i = 0
    while True:
        tree+=encoded_data[i]
        if encoded_data[i] == '}':
            encoded_data = encoded_data[i+1::]
            break
        i+=1

    input_string = ''.join(format(ord(i), '08b') for i in encoded_data)

    # with open(path+'tree.txt') as f:
    #     data = f.read()
    tree = json.loads(tree)
    chars = list(tree.keys())
    freq = list(tree.values())
    return decode_huffman(input_string, chars, freq)
    # return input_string

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
    # print(decode)
    return decode; 
