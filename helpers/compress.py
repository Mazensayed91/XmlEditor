import re
from utils import read_xml, to_json

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


def encode(path):
    binary_file = open("minimized.txt", "w")
    xml_data = read_xml(path)
    binary_huffman_tree, freq = huffman_compress(xml_data)
    print(binary_huffman_tree)
    big_text = ""
    for char in xml_data:
        big_text += binary_huffman_tree[char]
        small_text = ''
        if len(big_text) >= 7:
            character = big_text[:7]
            big_text = big_text[7:]
            character = int('0b' + character, 2)
            binary_char = character.to_bytes((character.bit_length() + 7) // 8, 'big').decode()
            small_text += binary_char
            binary_file.write(binary_char)

    # binary_int = int(big_text, 2)
    # byte_number = binary_int.bit_length() + 7 // 8
    # binary_array = binary_int.to_bytes(byte_number, "big")
    # ascii_text = binary_array.decode()
    # print(ascii_text)
    print(big_text)

    # to_json(freq, "freq")
    binary_file.close()


def decode(path):
    binary_file = open("minimized.txt", "r")
    encoded_data = binary_file.read()
    input_string = bin(int.from_bytes(encoded_data.encode(), 'big'))
    return input_string
